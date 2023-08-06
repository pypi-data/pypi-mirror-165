"""
 Author: yican.yc
 Date: 2022-08-23 19:25:15
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:25:15
"""
import gc
import os
from abc import abstractmethod
from timeit import default_timer as timer

import psutil
import torch.nn.functional as F

import numpy as np
import torch
from torch import optim
from torch.utils.data import IterableDataset
from torch.optim.lr_scheduler import CosineAnnealingLR, CyclicLR
from transformers import get_cosine_schedule_with_warmup, get_linear_schedule_with_warmup
from torch.optim import AdamW
from .callbacks import CallbackManager, EpochSchedulerCallback, SchedulerCallback, StepSchedulerCallback
from .utils.log_utils import init_logger
from .utils.optimizer_utils import get_3_stage_scheduler, get_llrd_model_parameters

from .utils.attacker_utils import FGM, PGD, AWP


class Trainer:
    def __init__(
        self,
        experiment_location=None,
        current_valid_fold=0,
        max_epochs=100,
        max_steps=None,
        num_eval_steps=20,
        optimizer_info='adamw~{"lr":2e-5}',
        scheduler_info="constant~{}",
        attacker_info="constant~{}",
        r_drop_info='{"start_ratio":np.inf, "alpha": 0.3}',  # 为空默认不做r-drop
        gradient_clip_val=0,
        gpus="0",
        precision="mixed",
        callbacks=[],
    ) -> None:
        # 为了callback记录参数
        self.experiment_location = experiment_location
        self.current_valid_fold = current_valid_fold
        self.max_epochs = max_epochs
        self.num_eval_steps = num_eval_steps
        self.global_step = 0
        self.max_steps = max_steps
        self.current_epoch = 0
        self.gpus = gpus
        self.precision = precision
        self.optimizer_info = optimizer_info
        self.scheduler_info = scheduler_info
        self.attacker_info = attacker_info
        self.r_drop_info = r_drop_info
        self.attacker_used = ""
        self.r_drop_used = ""
        assert self.precision in ("mixed", "32"), "precision should in [mixed, 32]"
        # https://pytorch.org/blog/accelerating-training-on-nvidia-gpus-with-pytorch-automatic-mixed-precision/
        # https://pytorch.org/docs/stable/notes/amp_examples.html#working-with-unscaled-gradients
        self.optimizer_name = str.lower(self.optimizer_info.split("~")[0])
        self.scheduler_name = str.lower(self.scheduler_info.split("~")[0])
        self.attacker_name = str.lower(self.attacker_info.split("~")[0])
        self.r_drop_parameters = eval(self.r_drop_info)
        try:
            self.optimizer_parameters = eval(self.optimizer_info.split("~")[1])
            self.scheduler_parameters = eval(self.scheduler_info.split("~")[1])
            self.attacker_parameters = eval(self.attacker_info.split("~")[1])
            if self.attacker_name != "constant":
                assert "start_ratio" in self.attacker_parameters, "start_ratio should in attacker_info"
                self.start_ratio = self.attacker_parameters.pop("start_ratio")
        except IndexError:
            raise ValueError(
                'optimizer_info,scheduler_name format example: adamw~{"lr":4e-5} | get_3_stage_scheduler~{}'
            )

        self.gradient_clip_val = gradient_clip_val
        # self.grad_clipper = AutoClipper()
        if len(self.gpus) == 0:
            self.DEVICE = torch.device(f"cuda:{self.gpus[0]}" if torch.cuda.is_available() else "cpu")
            if self.DEVICE == "cpu":
                raise ValueError("不要在CPU上跑深度学习程序!")
        else:
            # todo dataparallel需要改造 https://pytorch.org/tutorials/intermediate/ddp_tutorial.html
            # https://gist.github.com/sgraaf/5b0caa3a320f28c27c12b5efeb35aa4c
            self.DEVICE = torch.device(f"cuda:{self.gpus[0]}" if torch.cuda.is_available() else "cpu")
            # self.DEVICE = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")
            # os.environ["CUDA_VISIBLE_DEVICES"] = ",".join([str(gpu) for gpu in self.gpus])
        if self.precision == "mixed":
            self.amp_scaler = torch.cuda.amp.GradScaler()
        self.logger = self._configure_logger()
        self.callback_manager = CallbackManager(trainer=self, callbacks=callbacks)
        self.metrics_manager = {}
        self._tensorboard_time = 0
        try:
            self.metrics_manager["fold"] = self.current_valid_fold
        except (Exception, KeyboardInterrupt):
            self.metrics_manager["fold"] = 0

    def _configure_logger(self):
        logger = init_logger(log_dir=self.experiment_location)
        return logger

    def configure_optimizers(self):
        if self.optimizer_parameters.get("dynamic_lr") is True:
            # parameters = create_dynamic_learning_rate(self.model)
            parameters = get_llrd_model_parameters(
                self.model,
                bottom_lr=self.optimizer_parameters.get("bottom_lr"),
                incremental_lr=self.optimizer_parameters.get("incremental_lr"),
            )
            self.optimizer_parameters.pop("dynamic_lr")
            self.optimizer_parameters.pop("bottom_lr")
            self.optimizer_parameters.pop("incremental_lr")
        else:
            if self.optimizer_name == "adamw":
                weight_decay = 0.1
                parameters_tmp = list(self.model.named_parameters())
                no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
                parameters = [
                    {
                        "params": [p for n, p in parameters_tmp if not any(nd in n for nd in no_decay)],
                        "weight_decay": weight_decay,
                    },
                    {"params": [p for n, p in parameters_tmp if any(nd in n for nd in no_decay)], "weight_decay": 0.0},
                ]
            else:
                parameters = self.model.parameters()

        if self.optimizer_name == "sgd".lower():
            optimizer = optim.SGD(parameters, **self.optimizer_parameters)
        elif self.optimizer_name == "adam".lower():
            optimizer = optim.Adam(parameters, **self.optimizer_parameters)
        elif self.optimizer_name == "adamw".lower():
            # optimizer, scheduler
            # optimizer = AdamW(optimizer_grouped_parameters, **self.optimizer_parameters)
            optimizer = AdamW(parameters, **self.optimizer_parameters)

        else:
            raise NotImplementedError(f"{self.optimizer_name} 还没实现")
        # self.logger.info(f"optimizer_name : {self.optimizer_name}")
        # self.logger.info(f"self.optimizer_parameters: {self.optimizer_parameters}")
        return optimizer

    def configure_scheduler(self):
        # https://www.kaggle.com/isbhargav/guide-to-pytorch-learning-rate-scheduling

        # need implement different scheduler，要配置step, epoch level的设置，全部添加到callback里面去
        # todo warmup这几个的参数要重构下
        if self.scheduler_parameters.get("num_training_samples") is None:
            if isinstance(self.train_dataloader.dataset, IterableDataset):
                self.num_training_steps = (
                    int(len(self.train_dataloader) * self.max_epochs) / self.train_dataloader.batch_size
                )
            else:
                self.num_training_steps = int(len(self.train_dataloader) * self.max_epochs)
        else:
            self.num_training_steps = (
                int(self.scheduler_parameters.get("num_training_samples") / self.train_dataloader.batch_size)
                * self.max_epochs
            )
        scheduler_mode = self.scheduler_parameters.get("mode", "epoch")
        assert scheduler_mode in ("epoch", "step"), "model should be in epoch or step"
        if "mode" in self.scheduler_parameters:
            self.scheduler_parameters.pop("mode")

        if "warm_up_rate" in self.scheduler_parameters:
            self.num_warmup_steps = int(self.num_training_steps * self.scheduler_parameters["warm_up_rate"])
            self.logger.info(
                f"num_warmup_steps : {self.num_warmup_steps}, "
                f"num_training_steps : {self.num_training_steps}, "
                f"shceduler_mode : {scheduler_mode}"
            )
        else:
            self.logger.info(f"num_training_steps : {self.num_training_steps}, shceduler_mode : {scheduler_mode}")

        if self.scheduler_name == "get_linear_schedule_with_warmup":
            scheduler = get_linear_schedule_with_warmup(
                self.optimizer,
                num_warmup_steps=self.num_warmup_steps,
                num_training_steps=self.num_training_steps,
            )
        elif self.scheduler_name == "get_cosine_schedule_with_warmup":
            scheduler = get_cosine_schedule_with_warmup(
                self.optimizer,
                num_warmup_steps=self.num_warmup_steps,
                num_training_steps=self.num_training_steps,
            )
        elif self.scheduler_name == "CyclicLR".lower():
            scheduler = CyclicLR(self.optimizer, **self.scheduler_parameters)
        elif self.scheduler_name == "get_3_stage_scheduler".lower():
            scheduler = get_3_stage_scheduler(self.optimizer, self.num_training_steps)
        elif self.scheduler_name == "CosineAnnealingLR".lower():
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, **self.scheduler_parameters)
        elif self.scheduler_name == "constant".lower():
            pass
        else:
            raise NotImplementedError(f"{self.scheduler_name} 还没实现")
        # for i, callback in enumerate(self.callback_manager.callbacks):
        #     if (
        #         isinstance(callback, SchedulerCallback)
        #         or isinstance(callback, EpochSchedulerCallback)
        #         or isinstance(callback, StepSchedulerCallback)
        #     ):
        #         self.callback_manager.callbacks.pop(i)
        self.remove_scheduler()
        if self.scheduler_name == "constant":
            scheduler_callback = SchedulerCallback()
        else:
            if scheduler_mode == "step":
                scheduler_callback = StepSchedulerCallback(scheduler=scheduler)
            else:
                scheduler_callback = EpochSchedulerCallback(scheduler=scheduler)
        self.callback_manager.callbacks.append(scheduler_callback)
        # self.logger.info(f"scheduler_name : {self.scheduler_name} | mode: {scheduler_mode}")
        # self.logger.info(self.callback_manager.callbacks)

    def configure_attacker(self):
        class ConstantAttacker:
            def attack(self):
                pass

            def restore(self):
                pass

        if self.attacker_name == "constant":
            attacker = ConstantAttacker()
        elif self.attacker_name == "fgm":
            attacker = FGM(trainer=self, **self.attacker_parameters)
        elif self.attacker_name == "pgd":
            attacker = PGD(trainer=self, **self.attacker_parameters)
        elif self.attacker_name == "awp":
            attacker = AWP(trainer=self, **self.attacker_parameters)

        # print(self.attacker_parameters)
        return attacker

    def compute_kl_loss(sefl, p, q, pad_mask=None):
        # r-drop使用
        p_loss = F.kl_div(F.log_softmax(p, dim=-1), F.softmax(q, dim=-1), reduction="none")
        q_loss = F.kl_div(F.log_softmax(q, dim=-1), F.softmax(p, dim=-1), reduction="none")

        # pad_mask is for seq-level tasks
        if pad_mask is not None:
            p_loss.masked_fill_(pad_mask, 0.0)
            q_loss.masked_fill_(pad_mask, 0.0)

        # You can choose whether to use function "sum" and "mean" depending on your task
        p_loss = p_loss.sum()
        q_loss = q_loss.sum()

        loss = (p_loss + q_loss) / 2
        return loss

    def remove_scheduler(self):
        for i, callback in enumerate(self.callback_manager.callbacks):
            if (
                isinstance(callback, SchedulerCallback)
                or isinstance(callback, EpochSchedulerCallback)
                or isinstance(callback, StepSchedulerCallback)
            ):
                self.callback_manager.callbacks.pop(i)

    def load_from_checkpoint(self):
        # load state dict, 暂时忽略保存的step 和 epoch
        raise NotImplementedError("load_from_checkpoint not implemented")

    def on_train_start(self):
        # TODO 多张GPU的时候logger需要改写下
        # todo 这里要初始话很多self的属性
        self.best_singal = ""
        self.optimizer = self.configure_optimizers()
        self.scheduler = self.configure_scheduler()
        self.attacker = self.configure_attacker()
        self.callback_manager.on_train_start()

    def on_train_end(self):
        self.callback_manager.on_train_end()
        self.logger.info(f"RAM memory {psutil.virtual_memory()[2]/100:3.2%} used")
        self.model = self.model.to("cpu")
        self._optimizer_to(self.optimizer, "cpu")
        self.model = None
        self.optimizer = None
        del self.model
        del self.optimizer
        gc.collect()
        self.logger.info(f"RAM memory {psutil.virtual_memory()[2]/100:3.2%} used")

    def _optimizer_to(self, optim, device):
        for param in optim.state.values():
            # Not sure there are any global tensors in the state dict
            if isinstance(param, torch.Tensor):
                param.data = param.data.to(device)
                if param._grad is not None:
                    param._grad.data = param._grad.data.to(device)
            elif isinstance(param, dict):
                for subparam in param.values():
                    if isinstance(subparam, torch.Tensor):
                        subparam.data = subparam.data.to(device)
                        if subparam._grad is not None:
                            subparam._grad.data = subparam._grad.data.to(device)

    def fit(self, model, train_dataloader, valid_dataloader=None):
        try:
            # 1. 加载一些字典或者其他东西
            # 2. 创建一些储存文件的目录
            self.train_results_folder = f"{self.experiment_location}/train_results"
            self.valid_results_folder = f"{self.experiment_location}/valid_results"
            self.test_results_folder = f"{self.experiment_location}/test_results"
            os.makedirs(self.train_results_folder, exist_ok=True)
            os.makedirs(self.valid_results_folder, exist_ok=True)
            os.makedirs(self.test_results_folder, exist_ok=True)
            start_time = timer()
            self.model = model.to(self.DEVICE)
            if len(self.gpus) > 1:
                self.model = torch.nn.DataParallel(self.model, device_ids=self.gpus)
            self.train_dataloader = train_dataloader
            self.valid_dataloader = valid_dataloader
            self.logger.info(f"Train Batch Size : {self.train_dataloader.batch_size}")
            if self.valid_dataloader is not None:
                self.logger.info(f"Valid Batch Size : {self.valid_dataloader.batch_size}")
            self.on_train_start()
            # restore gloabl_step from checkpoint
            while self.current_epoch < self.max_epochs:
                self._train_one_epoch(train_dataloader=self.train_dataloader, valid_dataloader=self.valid_dataloader)
        except (Exception, InterruptedError):
            # todo 这里做cv的话会有问题
            # os.system(f"mv {self.experiment_location} {self.experiment_location}-failed")
            raise
        finally:
            # hanlde memory leak when do cross validation
            self.on_train_end()
            self.logger.info(f"Total training time: {int(timer() - start_time)} seconds")

    @abstractmethod
    def training_step(self, batch):
        raise NotImplementedError("You should implement training_step")

    def validation_step(self, batch):
        raise NotImplementedError("You should implement validation_step")

    def test_step(self, batch):
        raise NotImplementedError("You should implement test_step")

    def _train_one_epoch(self, train_dataloader, valid_dataloader):
        self.model.train()
        self.metrics_manager["epoch"] = self.current_epoch
        self.train_loss = AverageMeter()  # loss tracker
        self.train_batch_time = AverageMeter()  # forward prop + back prop time tracker
        self.train_load_time = AverageMeter()  # data loading time tracker
        self.num_train_batches = len(train_dataloader)
        start_time = timer()
        # todo 实现在整个epoch level求metric的功能
        for batch_idx, batch in enumerate(train_dataloader):
            self.train_batch_idx = batch_idx
            assert isinstance(batch, dict), "batch should be a dict"
            # Step-1: 清空梯度必须要在第一步做掉
            self.optimizer.zero_grad()
            # self.optimizer.zero_grad(set_to_none=True)

            # Step-2: 计算[一个batch数据]的加载时间
            self.train_load_time.update(value=timer() - start_time)

            # Step-3: 计算当前批次样本量
            try:
                batch_size = batch[list(batch.keys())[0]].shape[0]
            except AttributeError:
                # batch的第一个元素可能是id组成的list
                batch_size = len(batch[list(batch.keys())[0]])

            # Step-4: 计算一个batch
            if self.precision == "mixed":
                with torch.cuda.amp.autocast():
                    batch_output = self.training_step(batch)
            else:
                batch_output = self.training_step(batch)

            # todo implement fp16 backward
            # Step-4: 反向传播
            try:
                # before_attacked_loss = batch_output["loss"]
                if self.precision == "mixed":
                    self.amp_scaler.scale(batch_output["loss"]).backward()
                else:
                    batch_output["loss"].backward()
            except Exception:
                raise ValueError(
                    'key "loss" should in the output of training_step, and the output of train step should be a dict'
                )
            ##########################################################################################
            # 攻击的具体实现
            ##########################################################################################
            if self.attacker_name != "constant" and (self.global_step >= (self.num_training_steps * self.start_ratio)):
                self.attacker_used = (" " + self.attacker_name).upper()
                batch_output = self.attacker.attack(batch)

            if self.global_step >= (self.num_training_steps * self.r_drop_parameters.get("start_ratio")):
                self.r_drop_used = " R-DROP"

            self.train_loss.update(value=batch_output["loss"].item(), n=batch_size)
            # Step-5: 梯度裁剪
            if self.gradient_clip_val > 0:
                # self.grad_clipper.clip_grad_norm_(self.model)
                if self.precision == "mixed":
                    self.amp_scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.gradient_clip_val)

            # Step-6: 优化
            if self.precision == "mixed":
                self.amp_scaler.step(self.optimizer)
                self.amp_scaler.update()
            else:
                self.optimizer.step()
            self.global_step += 1
            self.metrics_manager["step"] = self.global_step
            self.metrics_manager["train_loss"] = self.train_loss.avg
            self.metrics_manager["lr"] = self.optimizer.param_groups[0]["lr"]
            self.train_batch_time.update(value=timer() - start_time)
            self.callback_manager.on_train_batch_end()
            if self.num_eval_steps != 0:
                # todo 这个逻辑是每隔 num_eval_steps 轮，不是每增加N轮
                if self.global_step % self.num_eval_steps == 0:
                    self._valid_one_epoch(dataloader=valid_dataloader)
                    if self.max_steps is not None:
                        if self.global_step > self.max_steps:
                            raise NotImplemented("仅仅用来测试最佳的valid batch_size大小")
            start_time = timer()
        self.callback_manager.on_train_epoch_end()
        # tensorboard 记录 histogram 会很花时间, 特地来记录, 默认记录 histogram 只会放在 on_train_epoch_end 后
        self._tensorboard_time = round(timer() - start_time, 1)
        if self.num_eval_steps == 0:
            self._valid_one_epoch(dataloader=valid_dataloader)
        self.current_epoch += 1
        self.on_train_epoch_end()

    def _valid_one_epoch(self, dataloader):
        # ========================================================================================================
        # 定义模型效果跟踪指标
        # ========================================================================================================
        if dataloader is None:
            pass
        else:
            self.model.eval()
            self.num_valid_batches = len(dataloader)
            # todo 实现在整个epoch level求metric的功能
            with torch.no_grad():
                self.valid_loss = AverageMeter()  # loss tracker
                self.valid_batch_time = AverageMeter()  # forward prop + back prop time tracker
                self.valid_load_time = AverageMeter()  # data loading time tracker
                outputs = []
                start_time = timer()
                for batch_idx, batch in enumerate(dataloader):
                    self.valid_batch_idx = batch_idx
                    assert isinstance(batch, dict), "batch should be a dict"
                    # Step-1: 计算[一个batch数据]的加载时间
                    self.valid_load_time.update(value=timer() - start_time)

                    # Step-2: 计算当前批次样本量
                    try:
                        batch_size = batch[list(batch.keys())[0]].shape[0]
                    except AttributeError:
                        # batch的第一个元素可能是id组成的list
                        batch_size = len(batch[list(batch.keys())[0]])

                    # Step-3: 计算一个batch
                    if self.precision == "mixed":
                        with torch.cuda.amp.autocast():
                            batch_output = self.validation_step(batch=batch)
                    else:
                        batch_output = self.validation_step(batch=batch)

                    # todo 怎么包装下让其更加灵活
                    for k in batch_output:
                        if isinstance(batch_output[k], torch.Tensor):
                            batch_output[k] = batch_output[k].detach().cpu()
                            if batch_output[k].dtype == torch.float16:
                                batch_output[k] = batch_output[k].double()
                    outputs.append(batch_output)

                    # Step-5: 更新待展示的 validation loss
                    try:
                        self.valid_loss.update(value=batch_output["loss"].item(), n=batch_size)
                    except Exception:
                        raise ValueError(
                            'key "loss" should in the output of validation_step, and the output of train step should be a dict'
                        )

                    # Step-11: 更新计算整个batch的平均时间
                    self.valid_batch_time.update(value=timer() - start_time)
                    start_time = timer()
                    self.callback_manager.on_valid_batch_end()
                self.metrics_manager["valid_loss"] = self.valid_loss.avg
                self.on_valid_epoch_end(outputs)
                self.callback_manager.on_valid_epoch_end()
                self._tensorboard_time = 0
            self.model.train()

    def on_train_epoch_end(self):
        # 暂时先不做实现，用不到，实现方式和on_valid_epoch_end类似
        pass

    def on_valid_epoch_end(self, outputs):
        """
        output template
        [{'y_pred': tensor([-0.7122, -1.1241, -0.0506, -1.5026, -0.1673, -1.0914]),
            'y': tensor([-0.5611, -1.7173,  0.0097, -2.1231,  0.2787, -1.7958, -0.1199,  0.6244]),
            'loss': tensor(0.7965)}]
        # 查看outputs的形状
        # import joblib
        # joblib.dump(outputs, "outputs.p")
        # cat would not create new dimension
        # stack would create new dimension
        """
        pass

    def test(self, model, dataloader, model_checkpoint=None, with_flag=True):
        # todo test right after fit, restore model_checkpoint on best
        # https://pytorch.org/tutorials/beginner/saving_loading_models.html
        self.model = model.to(self.DEVICE)
        if model_checkpoint is not None:
            self.model.load_state_dict(torch.load(model_checkpoint, map_location=self.DEVICE))
        self.model.eval()
        self.num_test_batches = len(dataloader)
        with torch.no_grad():
            self.test_loss = AverageMeter()  # loss tracker
            self.test_batch_time = AverageMeter()  # forward prop + back prop time tracker
            self.test_load_time = AverageMeter()  # data loading time tracker
            outputs = []
            start_time = timer()
            for batch_idx, batch in enumerate(dataloader):
                self.test_batch_idx = batch_idx
                assert isinstance(batch, dict), "batch should be a dict"
                # Step-1: 计算[一个batch数据]的加载时间
                self.test_load_time.update(value=timer() - start_time)

                # Step-2: 计算当前批次样本量
                try:
                    batch_size = batch[list(batch.keys())[0]].shape[0]
                except AttributeError:
                    # batch的第一个元素可能是id组成的list
                    batch_size = len(batch[list(batch.keys())[0]])

                # Step-3: 计算一个batch
                if self.precision == "mixed":
                    with torch.cuda.amp.autocast():
                        batch_output = self.test_step(batch=batch)
                else:
                    batch_output = self.test_step(batch=batch)

                # todo 怎么包装下让其更加灵活
                for k in batch_output:
                    if isinstance(batch_output[k], torch.Tensor):
                        batch_output[k] = batch_output[k].detach().cpu()
                        if batch_output[k].dtype == torch.float16:
                            batch_output[k] = batch_output[k].double()
                outputs.append(batch_output)

                # Step-5: 更新待展示的 test loss
                if with_flag is True:
                    try:
                        self.test_loss.update(value=batch_output["loss"].item(), n=batch_size)
                    except Exception:
                        raise ValueError(
                            'key "loss" should in the output of test_step, and the output of train step should be a dict'
                        )

                # Step-11: 更新计算整个batch的平均时间
                self.test_batch_time.update(value=timer() - start_time)
                start_time = timer()
                self.callback_manager.on_valid_batch_end()
            if with_flag is True:
                self.metrics_manager["test_loss"] = self.test_loss.avg
            return self.on_test_epoch_end(outputs)

    def on_test_epoch_end(self, outputs):
        """
        output template
        [{'y_pred': tensor([-0.7122, -1.1241, -0.0506, -1.5026, -0.1673, -1.0914]),
            'y': tensor([-0.5611, -1.7173,  0.0097, -2.1231,  0.2787, -1.7958, -0.1199,  0.6244]),
            'loss': tensor(0.7965)}]
        # 查看outputs的形状
        # import joblib
        # joblib.dump(outputs, "outputs.p")
        """
        pass


class AverageMeter(object):
    """Keeps track of most recent, average, sum, and count of a metric.

    Example
    -------
    losses = AverageMeter()
    losses.update(1, 5)
    print(losses.avg)
    """

    def __init__(self):
        self.reset()

    def reset(self):
        # Reset all value to 0.
        self.value = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, value, n=1):
        """Update value, average, sum, and count.

        Parameters
        ----------
        n : int, optional (default = 5)
        value : double

        """
        self.value = value
        self.sum += value * n
        self.count += n
        self.avg = self.sum / self.count
