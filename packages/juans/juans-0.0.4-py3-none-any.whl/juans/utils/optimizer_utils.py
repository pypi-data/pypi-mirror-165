"""
 Author: yican.yc
 Date: 2022-08-23 19:24:56
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:24:56
"""
import torch


def get_3_stage_scheduler(optimizer, total_train_steps):
    # two schedules:
    # 1. custom is similar to linear decay with warmup
    # 2. 3stage is simply halving every 1/3 steps
    def lr_lambda_2(step):
        if step <= total_train_steps * (1 / 3):
            return 1
        if step <= total_train_steps * (2 / 3):
            return 0.5
        if step <= total_train_steps * (3 / 3):
            return 0.25

    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda_2)


def get_llrd_model_parameters(model, bottom_lr=2e-5, incremental_lr=1e-5, weight_decay=0.01):
    """
    llrd : layer-wise learning rate decay
    """
    opt_parameters = []  # To be passed to the optimizer (only parameters of the layers you want to update).
    named_parameters = list(model.named_parameters())

    # According to AAAMLP book by A. Thakur, we generally do not use any decay
    # for bias and LayerNorm.weight layers.
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    set_4_7 = ["layer.4", "layer.5", "layer.6", "layer.7"]
    set_8_11 = ["layer.8", "layer.9", "layer.10", "layer.11"]
    set_12_15 = ["layer.12", "layer.13", "layer.14", "layer.15"]
    set_16_19 = ["layer.16", "layer.17", "layer.18", "layer.19"]
    set_20_23 = ["layer.20", "layer.21", "layer.22", "layer.23"]

    for i, (name, params) in enumerate(named_parameters):

        weight_decay_inner = 0.0 if any(p in name for p in no_decay) else weight_decay

        if ("embeddings" in name) or ("encoder" in name):
            # For layer 0 - 3 + embedding
            lr = bottom_lr
            # others
            lr = bottom_lr + incremental_lr if any(p in name for p in set_4_7) else lr
            lr = bottom_lr + incremental_lr * 2 if any(p in name for p in set_8_11) else lr
            lr = bottom_lr + incremental_lr * 3 if any(p in name for p in set_12_15) else lr
            lr = bottom_lr + incremental_lr * 4 if any(p in name for p in set_16_19) else lr
            lr = bottom_lr + incremental_lr * 5 if any(p in name for p in set_20_23) else lr

            opt_parameters.append({"params": params, "weight_decay": weight_decay_inner, "lr": lr})

        # For regressor and pooler, set lr to 0.0000036 (slightly higher than the top layer).
        else:
            lr = bottom_lr

            opt_parameters.append({"params": params, "weight_decay": weight_decay_inner})

    assert len(named_parameters) == len(opt_parameters), "LLRD的权重层数不对"
    return opt_parameters
