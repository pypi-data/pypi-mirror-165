"""
 Author: yican.yc
 Date: 2022-08-23 19:26:07
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:26:07
"""
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class RMSELoss(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.loss = torch.nn.MSELoss()

    def forward(self, input, target):
        assert input.shape == target.shape, f"loss input shape error, input {input.shape} | target {target.shape} !"
        return torch.sqrt(self.loss(input, target))


def MultilabelCategoricalCrossentropy(y_pred, y_true):
    y_pred = (1 - 2 * y_true) * y_pred  # -1 -> pos classes, 1 -> neg classes
    y_pred_neg = y_pred - y_true * 1e12  # mask the pred outputs of pos classes
    y_pred_pos = y_pred - (1 - y_true) * 1e12  # mask the pred outputs of neg classes
    zeros = torch.zeros_like(y_pred[..., :1])
    y_pred_neg = torch.cat([y_pred_neg, zeros], dim=-1)
    y_pred_pos = torch.cat([y_pred_pos, zeros], dim=-1)
    neg_loss = torch.logsumexp(y_pred_neg, dim=-1)
    pos_loss = torch.logsumexp(y_pred_pos, dim=-1)
    return (neg_loss + pos_loss).mean()


class Poly1CrossEntropyLoss(nn.Module):
    # https://blog.ceshine.net/post/polyloss/
    def __init__(self, epsilon: float = 1.0, reduction: str = "mean", weight: Optional[Tensor] = None):
        super(Poly1CrossEntropyLoss, self).__init__()
        self.epsilon = epsilon
        self.reduction = reduction
        self.weight = weight

    def forward(self, input, target, **kwargs):
        if input.dim() == 1:
            input = input.unsqueeze(0)
        probs = F.softmax(input, dim=-1)
        if self.weight is not None:
            self.weight = self.weight.to(target.device)
            probs = probs * self.weight.unsqueeze(0) / self.weight.mean()
        if target.dim() > 1:
            pt = torch.gather(probs, -1, target.argmax(1).unsqueeze(1))[:, 0]
        else:
            pt = torch.gather(probs, -1, target.unsqueeze(1))[:, 0]

        CE = F.cross_entropy(input=input, target=target, reduction="none", weight=self.weight)
        poly1 = CE + self.epsilon * (1 - pt)
        if self.reduction == "mean":
            poly1 = poly1.mean()
        elif self.reduction == "sum":
            poly1 = poly1.sum()
        return poly1
