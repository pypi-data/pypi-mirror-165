"""
 Author: yican.yc
 Date: 2022-08-23 19:24:24
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:24:24
"""
import torch


class FGM:
    def __init__(self, trainer, emb_name="word_embeddings.", epsilon=1e-8):
        """https://zhuanlan.zhihu.com/p/103593948
            做的事情就是在输入数据不变的情况下将原本的梯度g, 改为g_hat
            1.计算x的前向loss、反向传播得到梯度 (backward, 这个一般在外部进行)
            2.根据embedding矩阵的梯度计算出r, 并加到当前embedding上, 相当于x+r (attack)
            3.计算x+r的前向loss, 反向传播得到对抗的梯度, 累加到(1)的梯度上 (backward)
            4.将embedding恢复为(1)时的值 (restore)
            5.根据(3)的梯度对参数进行更新 (optimizer.step, 这个一般在外部进行)

        Args:
            model (_type_): _description_
            emb_name (str, optional): _description_. Defaults to "word_embeddings.".
            epsilon (_type_, optional): _description_. Defaults to 1e-8.
        """
        self.trainer = trainer
        self.weight_backup = {}
        self.epsilon = epsilon
        self.emb_name = emb_name

    def attack(self, batch):
        # 总体思想 : 产生基于某种扰动的梯度, 然后基于原始的权重更新整个网络
        self.attack_one_step()  # 将被攻击层(embedding)的权重添加基于梯度的扰动
        batch_output = self.generate_new_gradient(batch)  # 利用新权重生成进行一次正反向传播, 产生新的梯度
        self.restore()  # 将攻击层(embedding)的权重恢复到攻击前的状态
        # 最后我们得到了, 后续需要根据通过step用新的梯度来更新原始的weights
        # 1. 添加扰动后新的梯度
        # 2. 基于新的梯度产生的新的loss
        # 3. 原始weights不变
        return batch_output

    def attack_one_step(self):
        # 将被攻击层(embedding)的权重添加基于梯度的扰动
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad and self.emb_name in name:
                self.weight_backup[name] = param.data.clone()
                norm = torch.norm(param.grad)
                if norm != 0 and not torch.isnan(norm):
                    r_at = self.epsilon * param.grad / norm
                    param.data.add_(r_at)

    def generate_new_gradient(self, batch):
        # 利用新权重生成进行一次正反向传播, 产生新的梯度
        # 正向传播 在添加扰动的样本上进行推理
        # 反向传播 在正常的梯度基础上,累加对抗训练的梯度
        if self.trainer.precision == "mixed":
            with torch.cuda.amp.autocast():
                batch_output = self.trainer.training_step(batch)
            self.trainer.amp_scaler.scale(batch_output["loss"]).backward()
        else:
            batch_output = self.trainer.training_step(batch)
            batch_output["loss"].backward()
        return batch_output

    def restore(self):
        # 将被攻击层(embedding)的权重恢复到攻击前的状态
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad and self.emb_name in name:
                assert name in self.weight_backup
                param.data = self.weight_backup[name]
        self.weight_backup = {}


class PGD:
    def __init__(self, trainer, num_attack_steps, epsilon=1, alpha=0.3, emb_name="word_embeddings."):
        """emb.
        'PGD~{"start_ratio": 0.5, "num_attack_steps": 3, "epsilon":1, "alpha":0.3}'
        https://zhuanlan.zhihu.com/p/103593948
        1.计算x的前向loss、反向传播得到梯度并备份
        对于每步t:
            2.根据embedding矩阵的梯度计算出r,并加到当前embedding上,相当于x+r(超出范围则投影回epsilon内)
            3.t不是最后一步: 将梯度归0,根据1的x+r计算前后向并得到梯度
            4.t是最后一步: 恢复(1)的梯度,计算最后的x+r并将梯度累加到(1)上
        5.将embedding恢复为(1)时的值
        6.根据(4)的梯度对参数进行更新

        Args:
            model (_type_): _description_
        """
        self.trainer = trainer
        self.num_attack_steps = num_attack_steps
        self.weight_backup = {}
        self.grad_backup = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.emb_name = emb_name

    def attack_one_step(self, step=0):
        # emb_name这个参数要换成你模型中embedding的参数名
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad and self.emb_name in name:
                if step == 0:
                    # 保存embedding最初始的权重
                    self.weight_backup[name] = param.data.clone()
                norm = torch.norm(param.grad)
                if norm != 0 and not torch.isnan(norm):
                    r_at = self.alpha * param.grad / norm
                    # 给权重添加扰动
                    param.data.add_(r_at)
                    # pgd的关键, 如果添加扰动后的权重相比于最初是的权重大于某个阈值,则进行缩放操作
                    param.data = self._project(name, param.data, self.epsilon)

    def restore(self):
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad and self.emb_name in name:
                assert name in self.weight_backup
                param.data = self.weight_backup[name]
        self.weight_backup = {}

    def _project(self, param_name, param_data, epsilon):
        r = param_data - self.weight_backup[param_name]
        # 如果走出扰动半径, 则映射回球面
        if torch.norm(r) > epsilon:
            r = epsilon * r / torch.norm(r)
        return self.weight_backup[param_name] + r

    def backup_grad(self):
        # 保存模型被攻击前的所有梯度
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad:
                if param.grad is None:
                    self.grad_backup[name] = None
                else:
                    self.grad_backup[name] = param.grad.clone()

    def restore_grad(self):
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad:
                param.grad = self.grad_backup[name]

    def attack(self, batch):
        self.backup_grad()  # 保存模型被攻击前的所有梯度
        for step_i in range(self.num_attack_steps):  # 攻击N次
            # 将被攻击层(embedding)的权重添加基于梯度的扰动, 如果走出扰动半径epsilon则映射回球面
            self.attack_one_step(step=step_i)
            if step_i < (self.num_attack_steps - 1):
                # 前 k-1 次,每次都需要清空梯度
                self.trainer.optimizer.zero_grad()
            else:
                # 低 k 次恢复到开始攻击前的梯度, 因为要基于扰动后的weight来对梯度进行累加
                self.restore_grad()

            # 利用新权重生成进行一次正反向传播, 产生新的梯度
            # 正向传播 在添加扰动的样本上进行推理
            # 反向传播 在正常的梯度基础上,累加对抗训练的梯度
            if self.trainer.precision == "mixed":
                with torch.cuda.amp.autocast():
                    batch_output = self.trainer.training_step(batch)
                self.trainer.amp_scaler.scale(batch_output["loss"]).backward()
            else:
                batch_output = self.trainer.training_step(batch)
                batch_output["loss"].backward()
        self.restore()  # 将被攻击层(embedding)的权重恢复到攻击前的状态
        # 最后我们得到了, 后续需要根据通过step用新的梯度来更新原始的weights
        # 1. 添加扰动后新的梯度
        # 2. 基于新的梯度产生的新的loss
        # 3. 原始weights不变
        return batch_output


class AWP:
    """
    Args:
    adv_param (str): 要攻击的layer name,一般攻击第一层或者全部weight参数效果较好
    adv_lr (float): 攻击步长,这个参数相对难调节,如果只攻击第一层embedding,一般用1比较好,全部参数用0.1比较好。
    adv_eps (float): 参数扰动最大幅度限制,范围(0~ +∞),一般设置(0,1)之间相对合理一点。
    adv_step (int): PGD 攻击次数的实现,一般一次攻击既可以有相对不错的效果,多步攻击需要精调adv_lr。
    """

    def __init__(
        self,
        trainer,
        adv_param="weight",
        adv_lr=0.001,
        adv_eps=0.2,
        adv_step=1,
    ):
        self.trainer = trainer
        self.adv_param = adv_param
        self.adv_lr = adv_lr
        self.adv_eps = adv_eps
        self.adv_step = adv_step
        self.weight_backup = {}
        self.backup_eps = {}

    def attack(self, batch):
        self._save()  # 保存攻击的参数权重
        for i in range(self.adv_step):
            self._attack_step()  # 在embedding上添加对抗扰动
            # y_pred_adv = self.trainer.model(x)
            # loss_adv = self.criterion(y_pred_adv, y.view(-1, 1))
            # self.trainer.optimizer.zero_grad()
            # loss_adv.backward()  # 反向传播,并在正常的grad基础上,累加对抗训练的梯度
            batch_output = self.generate_new_gradient(batch)
        self._restore()  # 恢复embedding参数
        return batch_output

    def generate_new_gradient(self, batch):
        # 利用新权重生成进行一次正反向传播, 产生新的梯度
        # 正向传播 在添加扰动的样本上进行推理
        # 反向传播 在正常的梯度基础上,累加对抗训练的梯度
        if self.trainer.precision == "mixed":
            with torch.cuda.amp.autocast():
                batch_output = self.trainer.training_step(batch)
            self.trainer.optimizer.zero_grad()
            self.trainer.amp_scaler.scale(batch_output["loss"]).backward()
        else:
            batch_output = self.trainer.training_step(batch)
            self.trainer.optimizer.zero_grad()
            batch_output["loss"].backward()
        return batch_output

    def _attack_step(self):
        e = 1e-6  # 定义一个极小值
        # emb_name这个参数要换成你模型中embedding的参数名
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad and param.grad is not None and self.adv_param in name:
                norm1 = torch.norm(param.grad)
                norm2 = torch.norm(param.data.detach())
                if norm1 != 0 and not torch.isnan(norm1):
                    r_at = self.adv_lr * param.grad / (norm1 + e) * (norm2 + e)
                    param.data.add_(r_at)
                    param.data = torch.min(torch.max(param.data, self.backup_eps[name][0]), self.backup_eps[name][1])

    def _save(self):
        # emb_name这个参数要换成你模型中embedding的参数名
        for name, param in self.trainer.model.named_parameters():
            if param.requires_grad and param.grad is not None and self.adv_param in name:
                # 保存原始参数
                if name not in self.weight_backup:
                    self.weight_backup[name] = param.data.clone()
                    grad_eps = self.adv_eps * param.abs().detach()
                    self.backup_eps[name] = (
                        self.weight_backup[name] - grad_eps,
                        self.weight_backup[name] + grad_eps,
                    )

    def _restore(
        self,
    ):
        # emb_name这个参数要换成你模型中embedding的参数名
        for name, param in self.trainer.model.named_parameters():
            if name in self.weight_backup:
                param.data = self.weight_backup[name]
        self.weight_backup = {}
        self.backup_eps = {}
