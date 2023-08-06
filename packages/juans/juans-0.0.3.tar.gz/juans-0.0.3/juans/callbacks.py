"""
 Author: yican.yc
 Date: 2022-08-23 19:25:43
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:25:43
"""
import glob
import json
import sys
import logging
import operator
import os
import platform
import re
import subprocess
import textwrap
from datetime import datetime
from pathlib import Path
from time import time
from timeit import default_timer as timer
from .utils.bwa_utils import AveragedModel, update_bn
import numpy as np

try:
    import nvidia_smi
except Exception:
    pass

# import pytorch_lightning as pl
import torch
from torch.utils.tensorboard import SummaryWriter


# ==============================================================================================================
# my own callbacks
# ==============================================================================================================
class Callback(object):
    def __init__(self):
        super().__init__()
        # 同一个函数里面, 有些callback的优先级要比其他的高, 比如model_checkpoint里面有个标识best_singal要先于logger生成
        self.priority = 10

    def on_train_start(self, trainer):
        pass

    def on_train_end(self, trainer):
        pass

    def on_train_batch_begin(self, trainer):
        pass

    def on_train_batch_end(self, trainer):
        pass

    def on_valid_batch_begin(self, trainer):
        pass

    def on_valid_batch_end(self, trainer):
        pass

    def on_train_epoch_begin(self, trainer):
        pass

    def on_train_epoch_end(self, trainer):
        pass

    def on_valid_epoch_begin(self, trainer):
        pass

    def on_valid_epoch_end(self, trainer):
        pass


class CallbackManager(object):
    def __init__(self, trainer, callbacks=None):
        super().__init__()
        self.trainer = trainer
        self.callbacks = self.prepare_callbacks(callbacks)

    def prepare_callbacks(self, callbacks):
        if not callbacks:
            return []
        if isinstance(callbacks, Callback):
            callbacks = [callbacks]
        elif isinstance(callbacks, list):
            if all([isinstance(cb, Callback) for cb in callbacks]) is not True:
                obj = [cb for cb in callbacks if not isinstance(cb, Callback)][0]
                for c in obj:
                    print(c)
                raise TypeError(f"CallbackManager仅调用Callback类型，{type(obj).__name__}当前子类类型为{type(obj)}")
        else:
            raise TypeError(f"CallbackManager调用回调的子类为list集合，且各子类类型为Callback类型。")
        callbacks = sorted(callbacks, key=operator.attrgetter("priority"))
        return callbacks

    def on_train_start(self):
        for callback in self.callbacks:
            callback.on_train_start(trainer=self.trainer)

    def on_train_end(self):
        for callback in self.callbacks:
            callback.on_train_end(trainer=self.trainer)

    def on_train_batch_begin(self):
        for callback in self.callbacks:
            callback.on_train_batch_begin(trainer=self.trainer)

    def on_train_batch_end(self):
        for callback in self.callbacks:
            callback.on_train_batch_end(trainer=self.trainer)

    def on_valid_batch_begin(self):
        for callback in self.callbacks:
            callback.on_valid_batch_begin(trainer=self.trainer)

    def on_valid_batch_end(self):
        for callback in self.callbacks:
            callback.on_valid_batch_end(trainer=self.trainer)

    def on_train_epoch_begin(self):
        for callback in self.callbacks:
            callback.on_train_epoch_begin(trainer=self.trainer)

    def on_train_epoch_end(self):
        for callback in self.callbacks:
            callback.on_train_epoch_end(trainer=self.trainer)

    def on_valid_epoch_begin(self):
        for callback in self.callbacks:
            callback.on_valid_epoch_begin(trainer=self.trainer)

    def on_valid_epoch_end(self):
        for callback in self.callbacks:
            callback.on_valid_epoch_end(trainer=self.trainer)


class LoggerCallback(Callback):
    def __init__(self, detail=False, monitor=None, enable_progress_bar=False):
        super().__init__()
        self.detail = detail
        self.monitor = monitor
        self.enable_progress_bar = enable_progress_bar
        self.start_time = timer()
        try:
            nvidia_smi.nvmlInit()
            self.handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
        except Exception:
            self.handle = None
        self.gb = 1024 * 1024 * 1024

    def on_train_start(self, trainer):
        trainer.best_singal = "*"
        try:
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(self.handle)
        except Exception:

            class FakeInfo:
                used = 0
                total = 0

            info = FakeInfo()
        # trainer.logger.info(vars(trainer.hparams))
        trainer.logger.info(f"experiment_location : {trainer.experiment_location}")
        trainer.logger.info(
            f'Fold {trainer.metrics_manager["fold"]}, Total gpus {torch.cuda.device_count()}, use gpu {trainer.gpus}'
            f", gpu memory {(info.total / self.gb):.2f}G"
        )
        trainer.logger.info(
            f"epoch  steps  learning_rate  |  train_loss  valid_loss  load_time  batch_time  metric  time_elapsed  gpu_used"
        )
        trainer.logger.info("-" * 108)
        trainer.bwa_weight_used = ""

    def on_valid_epoch_end(self, trainer):
        try:
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(self.handle)
        except Exception:

            class FakeInfo:
                used = 0
                total = 0

            info = FakeInfo()
        if trainer.num_eval_steps == 0:
            train_load_time = trainer.train_load_time.sum
            train_batch_time = trainer.train_batch_time.sum
        else:
            train_load_time = trainer.train_load_time.avg * trainer.num_eval_steps
            train_batch_time = trainer.train_batch_time.avg * trainer.num_eval_steps

        for k, v in trainer.metrics_manager.items():
            if isinstance(v, torch.Tensor):
                trainer.metrics_manager[k] = v.item()
        if self.detail is True:
            if trainer.current_epoch == trainer.max_epochs:
                bwa_flag = " BWA"
            else:
                bwa_flag = ""
            time_elapsed_second = int(timer() - self.start_time)
            time_elapsed = f"{round( time_elapsed_second / 60)} m {time_elapsed_second % 60} s"
            trainer.logger.info(
                f"{str(trainer.current_epoch)+trainer.best_singal:<7s}"
                f"{str(trainer.global_step):<7s}"
                f'{str(round(trainer.metrics_manager["lr"], 8)):<14s} |  '
                f'{str(round(trainer.metrics_manager["train_loss"], 4)):<12s}'
                f'{str(round(trainer.metrics_manager["valid_loss"], 4)):<12s}'
                f'{(str(round(train_load_time, 1)) + " " + str(round(trainer.valid_load_time.sum, 1))):<11s}'
                f'{(str(round(train_batch_time, 1)) + " " + str(round(trainer.valid_batch_time.sum, 1))  + " " +  str(trainer._tensorboard_time)):<11s}'
                f"{str(round(trainer.metrics_manager[self.monitor], 4)):<12s}"
                f"{time_elapsed:<12s}"
                f"{(info.used / self.gb):.2f}G" + trainer.attacker_used + trainer.r_drop_used + trainer.bwa_weight_used
            )
        else:
            if trainer.current_epoch == trainer.max_epochs:
                bwa_flag = " BWA"
            else:
                bwa_flag = ""
            time_elapsed = f"{round((timer() - self.start_time) / 60, 2)} min"
            trainer.logger.info(
                f"{str(trainer.current_epoch)+trainer.best_singal:<7s}"
                f"{str(trainer.global_step):<7s}"
                f'{str(round(trainer.metrics_manager["lr"], 8)):<14s} |  '
                f'{str(round(trainer.metrics_manager["train_loss"], 4)):<12s}'
                f'{str(round(trainer.metrics_manager["valid_loss"], 4)):<12s}'
                f'{(str(round(trainer.valid_load_time.sum + train_load_time, 1)) + " s"):<11s}'
                f'{(str(round(trainer.valid_batch_time.sum + train_batch_time + trainer._tensorboard_time, 1)) + " s"):<12s}'
                f"{str(round(trainer.metrics_manager[self.monitor], 4)):<12s}"
                f"{time_elapsed:<12s}"
                f"{(info.used / self.gb):.2f}G" + trainer.attacker_used + trainer.r_drop_used + trainer.bwa_weight_used
            )
            trainer.bwa_weight_used = ""

    def on_train_batch_end(self, trainer):
        # print(trainer.train_batch_idx, trainer.num_train_batches)
        if self.enable_progress_bar is True:
            print(
                f"Train Progress {trainer.train_batch_idx / trainer.num_train_batches:.2%}" + "\r", end="", flush=True
            )

    def on_valid_batch_end(self, trainer):
        if self.enable_progress_bar is True:
            print(
                f"Valid Progress {trainer.valid_batch_idx / trainer.num_valid_batches:.2%}" + "\r", end="", flush=True
            )

    def on_test_batch_end(self, trainer):
        if self.enable_progress_bar is True:
            print(f"Test Progress {trainer.test_batch_idx / trainer.num_test_batches:.2%}" + "\r", end="", flush=True)


class LoggerCallbackTabular(Callback):
    def __init__(self, detail=False, monitor=None):
        super().__init__()
        self.detail = detail
        self.monitor = monitor
        self.start_time = timer()
        try:
            import nvidia_smi

            nvidia_smi.nvmlInit()
            self.handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
        except Exception:
            self.handle = None
        self.gb = 1024 * 1024 * 1024

    def on_train_start(self, trainer):
        trainer.best_singal = "*"
        try:
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(self.handle)
        except Exception:

            class FakeInfo:
                used = 0
                total = 0

            info = FakeInfo()
        # trainer.logger.info(vars(trainer.hparams))
        trainer.logger.info(f"experiment_location : {trainer.experiment_location}")
        trainer.logger.info(
            f'Fold {trainer.metrics_manager["fold"]}, Total gpus {torch.cuda.device_count()}, use gpu {trainer.gpus}'
            f"gpu memory {(info.total / self.gb):.2f}G"
        )
        trainer.logger.info(
            f"epoch  steps  learning_rate  |  train_loss  valid_loss  load_time  batch_time  metric  time_elapsed gpu_used"
        )
        trainer.logger.info("-" * 85)

    def on_valid_epoch_end(self, trainer):
        try:
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(self.handle)
        except Exception:

            class FakeInfo:
                used = 0
                total = 0

            info = FakeInfo()
        if trainer.num_eval_steps == 0:
            train_load_time = trainer.train_load_time.sum
            train_batch_time = trainer.train_batch_time.sum
        else:
            train_load_time = trainer.train_load_time.avg * trainer.num_eval_steps
            train_batch_time = trainer.train_batch_time.avg * trainer.num_eval_steps
        if self.detail is True:
            if trainer.current_epoch == trainer.max_epochs:
                bwa_flag = " BWA"
            else:
                bwa_flag = ""
            time_elapsed = f"{round((timer() - self.start_time) / 60, 2)} min"
            trainer.logger.info(
                f"{str(trainer.current_epoch)+trainer.best_singal:<7s}"
                f"{str(trainer.global_step):<7s}"
                f'{str(round(trainer.metrics_manager["lr"], 8)):<14s} |  '
                f'{str(round(trainer.metrics_manager["train_loss"], 4)):<12s}'
                f'{str(round(trainer.metrics_manager["valid_loss"], 4)):<12s}'
                f'{(str(round(train_load_time, 1)) + " " + str(round(trainer.valid_load_time.sum, 1))):<11s}'
                f'{(str(round(train_batch_time, 1)) + " " + str(round(trainer.valid_batch_time.sum, 1))  + " " +  str(trainer._tensorboard_time)):<11s}'
                f"{str(round(trainer.metrics_manager[self.monitor], 4)):<12s}"
                f"{time_elapsed:<12s}"
                f'{str(trainer.metrics_manager["recalls"])}'
                f"{(info.used / self.gb):.2f}G" + bwa_flag
            )
        else:
            if trainer.current_epoch == trainer.max_epochs:
                bwa_flag = " BWA"
            else:
                bwa_flag = ""
            time_elapsed = f"{round((timer() - self.start_time) / 60, 2)} min"
            trainer.logger.info(
                f"{str(trainer.current_epoch)+trainer.best_singal:<7s}"
                f"{str(trainer.global_step):<7s}"
                f'{str(round(trainer.metrics_manager["lr"], 8)):<14s} |  '
                f'{str(round(trainer.metrics_manager["train_loss"], 4)):<12s}'
                f'{str(round(trainer.metrics_manager["valid_loss"], 4)):<12s}'
                f'{(str(round(trainer.valid_load_time.sum + train_load_time, 1)) + " s"):<11s}'
                f'{(str(round(trainer.valid_batch_time.sum + train_batch_time + trainer._tensorboard_time, 1)) + " s"):<12s}'
                f"{str(round(trainer.metrics_manager[self.monitor], 4)):<12s}"
                f"{time_elapsed:<12s}"
                f'{str(trainer.metrics_manager["recalls"])}'
                f"{(info.used / self.gb):.2f}G" + bwa_flag
            )


class BWACallback(Callback):
    def __init__(self, model, weighted_ratio, start_ratio, model_forward_func):
        """_summary_

        Args:
            model : pytorch模型
            weighted_ratio (float): 当前轮次模型参数的权重
            start_ratio (_type_): bwa从训练的什么阶段开始执行, 例如0.1的话则为从10% gloab_steps开始收集权重
            model_forward_func (function): model前项推理的函数, 必须是input作为key
                def model_forward_func(model, input):
                    model(input_ids=input["input_ids"], attention_mask=input["attention_mask"]
        """
        super().__init__()
        self.priority = 1
        # 参数加权的策略
        self.ema_avg = (
            lambda averaged_model_parameter, model_parameter, num_averaged: (1 - weighted_ratio)
            * averaged_model_parameter
            + weighted_ratio * model_parameter
        )
        self.model = model
        # 模型前项推理的函数
        self.model_forward_func = model_forward_func
        # 什么时候开始执行策略
        self.start_ratio = start_ratio

    def on_train_start(self, trainer):
        # 参数加权后的模型, 放到这里是因为model的device是自动产生的, 这里为了让 AveragedModel和model放到同一device上
        self.bwa_model = AveragedModel(self.model, avg_fn=self.ema_avg)
        trainer.save_bwa_model = False
        trainer.bwa_weight_used = ""

    def on_train_end(self, trainer):
        # 更新batchnorm参数
        update_bn(
            trainer.train_dataloader,
            self.bwa_model,
            model_forward_func=self.model_forward_func,
            device=trainer.DEVICE,
        )
        # 我这里会给trainer一个信号去保存bwa的最后一个权重, 中间的权重不会做任何保存
        trainer.save_bwa_model = True
        # 验证bwa在valid上的效果并进行保存
        trainer.model = self.bwa_model
        trainer._valid_one_epoch(dataloader=trainer.valid_dataloader)
        # 清空显存
        self.bwa_model = self.bwa_model.to("cpu")
        self.bwa_model = None
        del self.bwa_model

    def on_valid_epoch_end(self, trainer):
        # trainer.best_singal是从ModelCheckpointCallback中传过来的，代表当前模型是此epoch为止最好的模型，
        # 所以ModelCheckpointCallback的执行顺序必须在BWACallback之前
        if trainer.best_singal == "*":
            if trainer.global_step >= trainer.num_training_steps * self.start_ratio:
                self.bwa_model.update_parameters(trainer.model)
                self.bwa_model.eval()
                # 信号传输给 LoggerCallback, 用于显示用BWA到了该模型
                trainer.bwa_weight_used = " BWA"


class ModelCheckpointCallback(Callback):
    def __init__(self, dirpath, file_name, monitor="valid_loss", mode="min", save_top_k=1, save_last=False):
        super().__init__()
        assert file_name[-4:] == "ckpt", "file_name must end with ckpt"
        self.dirpath = dirpath
        self.file_name = file_name
        self.monitor = monitor
        self.mode = mode
        self.save_top_k = save_top_k
        self.save_last = save_last

        if mode == "min":
            self.monitor_op = np.less
            self.best_loss_or_score = np.Inf
        elif mode == "max":
            self.monitor_op = np.greater
            self.best_loss_or_score = -np.Inf

        self.current_time = time()
        self.priority = 0
        self.only_format_once = True

    def on_train_start(self, trainer):
        os.makedirs(self.dirpath, exist_ok=True)

    def _smart_save(self, trainer):
        try:
            if trainer.save_bwa_model is True:
                trainer.best_model_path = self.best_model_path = os.path.join(
                    self.dirpath, "bwa-" + self.file_name_inner
                )
                torch.save(trainer.model.module.state_dict(), self.best_model_path)
        except Exception:
            trainer.logger.info("save bwa weights error.")

        if trainer.save_bwa_model is False:
            trainer.best_model_path = self.best_model_path = os.path.join(self.dirpath, self.file_name_inner)
            if len(trainer.gpus) > 1:
                torch.save(trainer.model.module.state_dict(), self.best_model_path)
            else:
                torch.save(trainer.model.state_dict(), self.best_model_path)

    def on_valid_epoch_end(self, trainer):
        # print(f"save_bwa_model: {trainer.save_bwa_model}")
        if self.monitor_op(trainer.metrics_manager[self.monitor], self.best_loss_or_score):
            self._auto_rename_filename(trainer=trainer)
            self._smart_save(trainer=trainer)
            self._keep_latest_checkpoint()
            self.best_loss_or_score = trainer.metrics_manager[self.monitor]
            trainer.best_singal = "*"
        else:
            trainer.best_singal = ""

        # if (trainer.swa is True) and (trainer.swa_info["mode"] == "last"):
        #     trainer.bwa_weight_used = " USE"
        #     if trainer.global_step >= trainer.num_training_steps * trainer.swa_info["swa_start_ratio"]:
        #         trainer.bwa_model.update_parameters(trainer.model)

    def _auto_rename_filename(self, trainer):
        groups = re.findall(r"(\{.*?)[:\}]", self.file_name)
        if len(groups) >= 0:
            if self.only_format_once is True:
                for group in groups:
                    name = group[1:]
                    self.file_name = self.file_name.replace(group, name + "={" + name)
                    if name not in trainer.metrics_manager:
                        trainer.metrics_manager[name] = 0
                self.only_format_once = False

            self.file_name_inner = self.file_name.format(**trainer.metrics_manager)

    def _keep_latest_checkpoint(self):
        """保存最近的max_to_keep个模型，其余模型将被删除"""
        ckpt_paths = glob.glob(os.path.join(self.dirpath, "*.ckpt"))
        avaliable_paths = [
            str(file_name)
            for file_name in list(Path(self.dirpath).iterdir())
            if ((os.path.getctime(str(file_name)) >= self.current_time) and ("last.ckpt" not in str(file_name)))
        ]
        avaliable_ckpt_paths = [path for path in ckpt_paths if path in avaliable_paths]
        saved_ckpt_paths = sorted(avaliable_ckpt_paths, key=os.path.getctime)[-self.save_top_k :]
        deleted_model_paths = set(avaliable_ckpt_paths).difference(saved_ckpt_paths)

        for path in deleted_model_paths:
            os.remove(path)


class TorchTensorboardCallback(Callback):
    """
    用于tensorboard相关监控数据输出, 包括输出
    text: 超参数
    hist,graph: 权重的图示
    profile: 用于剖析性能瓶颈的页面

    pytorch lightning Callback文档
    https://pytorch-lightning.readthedocs.io/en/latest/extensions/callbacks.html
    pytorch lightning Callback源码
    https://github.com/PyTorchLightning/pytorch-lightning/blob/7eff00317d53054a426cf3c186e01702377869d3/pytorch_lightning/callbacks/base.py
    callback 流程图
    https://github.com/PyTorchLightning/pytorch-lightning/blob/f407a00cec59886cbaf8816630f6760e34926bd5/docs/source/common/lightning_module.rst
    """

    def __init__(self, hparams, experiment_location, profiler=None, add_weight_and_histogram=False):
        super().__init__()
        self.profiler = profiler
        self.hparams = hparams
        self.add_weight_and_histogram = add_weight_and_histogram
        self.writer = SummaryWriter(log_dir=os.path.join(experiment_location, "tb_logger"))
        # https://pytorch.org/docs/stable/tensorboard.html

    def on_train_start(self, trainer):
        """以json format 的 text 记录超参数"""

        # 记录参数
        self.writer.add_text("hparams", self._pretty_json(self.hparams))

    def on_train_batch_end(self, trainer):
        """pytorch profiler 分析程序性能的关键代码"""
        # 记录profiler文件
        if self.profiler is not None:
            self.profiler.step()

        if trainer.num_eval_steps != 0:
            if trainer.global_step % trainer.num_eval_steps == 0:
                # 记录除epoch step fold外的所有其他参数
                for metric in trainer.metrics_manager:
                    if (metric not in ["epoch", "step", "fold"]) and (
                        isinstance(trainer.metrics_manager[metric], (float, int))
                    ):
                        self.writer.add_scalar(metric, trainer.metrics_manager[metric], trainer.global_step)

    def on_train_epoch_end(self, trainer):
        # 记录梯度和权重, 这个开销比较大，频率要低一点
        if self.add_weight_and_histogram:
            for name, params in trainer.model.named_parameters():
                self.writer.add_histogram(name, params, trainer.global_step)
                if params.requires_grad:
                    try:
                        self.writer.add_histogram(name + ".grad", params.grad, trainer.global_step)
                    except Exception:
                        pass

        if trainer.num_eval_steps == 0:
            # 记录除epoch step fold外的所有其他参数
            for metric in trainer.metrics_manager:
                # and type(trainer.metrics_manager[metric]) not in (list)
                if (metric not in ["epoch", "step", "fold"]) and (
                    isinstance(trainer.metrics_manager[metric], (float, int))
                ):
                    self.writer.add_scalar(metric, trainer.metrics_manager[metric], trainer.global_step)

    def on_train_end(self, trainer):
        self.writer.close()

    def _pretty_json(self, hp):
        # tensorboard以json的格式显示文本
        json_hp = json.dumps(vars(hp), indent=2)
        return "".join("\t" + line for line in json_hp.splitlines(True))


class SchedulerCallback(Callback):
    def __init__(self):
        super().__init__()

    def on_backward_end(self, trainer):
        pass

    def on_train_epoch_end(self, trainer):
        pass


class StepSchedulerCallback(Callback):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    def on_train_batch_end(self, trainer):
        self.scheduler.step()


class EpochSchedulerCallback(Callback):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    def on_train_epoch_end(self, trainer):
        self.scheduler.step()


class DynamicEvaluationStrategyCallback(Callback):
    def __init__(self):
        super().__init__()

    def on_valid_epoch_end(self, trainer):
        # commonlit : 48 * 10 = 480
        EVAL_SCHEDULE = [(np.power(0.5, 2), 10), (np.power(0.44, 2), 5)]
        for loss, period in EVAL_SCHEDULE:
            if trainer.valid_loss.avg >= loss:
                trainer.num_eval_steps = period
                break


class OssSync:
    # https://help.aliyun.com/document_detail/256352.html
    def __init__(
        self,
        local_dir: str,
        oss_dir: str,
        config_dir: str,
        ossutil_path: str = None,
        endpoint: str = "http://oss-cn-hangzhou-zmf.aliyuncs.com",
        aid: str = None,
        akey: str = None,
        create_oss_folder=True,
        download_ossutil_timeout: int = 120,
        sync_timeout: int = 360,
        verbose=False,
    ):
        self.verbose = verbose
        self.local_dir = local_dir
        self.oss_dir = oss_dir
        self.download_ossutil_timeout = download_ossutil_timeout
        self.sync_timeout = sync_timeout
        self.init_config_info(endpoint, aid, akey)
        if not ossutil_path:
            self.ossutil_path = self.download_ossutil()
        else:
            self.ossutil_path = ossutil_path
        _ = subprocess.run(["chmod", "755", ossutil_path], check=True, timeout=120)

        self.config_file_path = os.path.join(
            os.path.abspath(config_dir), f"ossutil_config_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        self.create_config_file(self.generate_config_content())
        if create_oss_folder:
            self.make_oss_dir()

    def init_config_info(self, endpoint: str = None, aid: str = None, akey: str = None):
        self.endpoint = endpoint
        self.aid = aid
        self.akey = akey

        if not self.endpoint:
            raise RuntimeError(f"请提供endpoint")
        if not aid:
            aid = os.getenv("ENV_ODPS_ACCESS_ID", "")
            if not aid:
                raise RuntimeError(f"找不到环境变量: ENV_ODPS_ACCESS_ID")
            self.aid = aid
        if not akey:
            akey = os.getenv("ENV_ODPS_ACCESS_KEY", "")
            if not akey:
                raise RuntimeError(f"找不到环境变量: ENV_ODPS_ACCESS_KEY")
            self.akey = akey
        # print(f"aid : {self.aid} | akey: {self.akey}")

    def generate_config_content(self) -> str:
        content = f"""
            [Credentials]
            language=EN
            endpoint={self.endpoint}
            accessKeyID={self.aid}
            accessKeySecret={self.akey}
        """
        return textwrap.dedent(content).strip()

    def create_config_file(self, config_content: str):
        with open(self.config_file_path, "wt") as f:
            f.write(config_content)

    def download_ossutil(
        self,
        download_dir: str = ".",
        ossutil_url_prefix: str = "http://gosspublic.alicdn.com/ossutil",
        version: str = "1.7.5",
        linux_file_name: str = "ossutil64",
        mac_file_name: str = "ossutilmac64",
    ) -> str:
        logging.info("Start to download ossuti ...")
        download_dir = os.path.abspath(download_dir)

        platform_system = platform.system()
        if platform_system == "Linux":
            ossutil_url = "/".join([ossutil_url_prefix, version, linux_file_name])
            ossutil_path = os.path.join(download_dir, linux_file_name)
            _ = subprocess.run(
                ["wget", "-t", "3", "-O", ossutil_path, ossutil_url], check=True, timeout=self.download_ossutil_timeout
            )
        elif platform_system == "Darwin":
            ossutil_url = "/".join([ossutil_url_prefix, version, mac_file_name])
            ossutil_path = os.path.join(download_dir, mac_file_name)
            _ = subprocess.run(
                ["curl", "-o", ossutil_path, ossutil_url], check=True, timeout=self.download_ossutil_timeout
            )
        else:
            raise RuntimeError(f"{platform_system}系统不支持")
        _ = subprocess.run(["chmod", "755", ossutil_path], check=True, timeout=120)
        logging.info("done")
        return ossutil_path

    def upload(self):
        if self.verbose is True:
            print(f"Download from {self.local_dir} to {self.oss_dir}")
        if os.path.exists(self.local_dir):
            try:
                _ = subprocess.run(
                    [
                        self.ossutil_path,
                        "sync",
                        self.local_dir,
                        self.oss_dir,
                        "--delete",
                        "--force",
                        "--update",
                        "-c",
                        self.config_file_path,
                    ],
                    stdout=subprocess.PIPE,
                    check=True,
                    timeout=self.sync_timeout,
                )
            except Exception:
                logging.error(f"上传到oss失败, returncode")
        else:
            logging.warning(f"本地目录{self.local_dir}不存在")

    def download(self, backup_dir):
        if self.verbose is True:
            print(f"Download from {self.oss_dir} to {self.local_dir}")
        try:
            _ = subprocess.run(
                [
                    self.ossutil_path,
                    "sync",
                    self.oss_dir,
                    self.local_dir,
                    "--delete",
                    "--force",
                    "--update",
                    "--backup-dir",
                    backup_dir,
                    "-c",
                    self.config_file_path,
                ],
                stdout=subprocess.PIPE,
                check=True,
                timeout=self.sync_timeout,
            )
        except Exception:
            logging.error(f"从oss下载失败")

    def make_oss_dir(self):
        _ = subprocess.run(
            [self.ossutil_path, "mkdir", self.oss_dir, "-c", self.config_file_path], check=True, timeout=120
        )


class Download2OssCallback(Callback):
    def __init__(self, osync):
        super().__init__()
        self.osync = osync

    # def on_train_epoch_end(self, trainer):
    #     self.osync.upload()

    def on_train_end(self, trainer):
        self.osync.upload()
