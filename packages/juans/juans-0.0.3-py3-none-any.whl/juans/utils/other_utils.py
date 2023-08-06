"""
 Author: yican.yc
 Date: 2022-08-23 19:25:00
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:25:00
"""
import json
import os
import random
from datetime import datetime

import numpy as np
import torch

# ==============================================================================================================
# 时间相关
# ==============================================================================================================
def get_current_time():
    return str(datetime.now()).split(".")[0].replace(" ", "-")


def seed_reproducer(seed=2019):
    """Reproducer for pytorch experiment.
    https://pytorch.org/docs/stable/notes/randomness.html
    # todo 可能需要按照文档添加workder的固定器
    Parameters
    ----------
    seed: int, optional (default = 2019)
        Radnom seed.

    Example
    -------
    seed_reproducer(seed=2019).
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.enabled = True


def pretty_json(hparams):
    # tensorboard以json的格式显示文本
    # if hparams
    if isinstance(hparams, dict):
        json_hp = json.dumps(hparams, indent=2)
    else:
        json_hp = json.dumps(vars(hparams), indent=2)
    return "".join("\t" + line for line in json_hp.splitlines(True))
