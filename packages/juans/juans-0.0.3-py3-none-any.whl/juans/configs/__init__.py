"""
 Author: yican.yc
 Date: 2022-08-23 19:23:42
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:23:42
"""
import ast
import os
import shutil
from argparse import ArgumentParser
from pathlib import Path

import torch

from ..callbacks import Download2OssCallback, OssSync
from ..utils.other_utils import get_current_time, pretty_json, seed_reproducer

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
ROOTFolder = "."


def get_list_of_files(dirName):
    # 获取当前目录下的所有文件名
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        allFiles.append(fullPath)
    return allFiles


def backup_code_folder(hparams):
    os.makedirs(f"{hparams.experiment_location}/codes", exist_ok=True)
    py_files = [file for file in get_list_of_files(ROOTFolder) if file.endswith("py")]
    for py_file in py_files:
        shutil.copy(py_file, f'{hparams.experiment_location}/codes/{py_file.split("/")[-1]}')
    shutil.copy("run.sh", f"{hparams.experiment_location}/codes/run.sh")


def exchange_oss_resource(
    server_expriment_folder,
    oss_expriment_folder,
    server_data_folder=None,
    oss_data_folder=None,
    server_weights_folder=None,
    oss_weights_folder=None,
    current_dir="/workspace/bin",
):
    """
    hparams.experiment_location : data/output/log/cifar10/08-18-20:02:07-no-name
    server_expriment_folder : 不存在的话会自动创建,
    oss_expriment_folder : 不存在的话会自动创建
    server_data_folder : 服务器存放数据的地方
    oss_data_folder : 可以把所有需要转移到服务器的数据资源都放到oss的该文件夹下
    server_weights_folder : 服务器存放权重的地方
    oss_weights_folder : oss存放权重的地方
    """
    # 上传文件夹至 oss_expriment_folder
    oss_expriment_folder_sync_uploader = OssSync(
        local_dir=server_expriment_folder,
        oss_dir=oss_expriment_folder,
        config_dir=current_dir,
        create_oss_folder=False,
        ossutil_path=f"{current_dir}/ossutil64",
    )
    oss_uploader_callback = Download2OssCallback(oss_expriment_folder_sync_uploader)

    if oss_data_folder is not None:
        # 下载数据至服务器 server_data_folder
        oss_data_downloader_sync = OssSync(
            local_dir=server_data_folder,
            oss_dir=oss_data_folder,
            config_dir=current_dir,
            ossutil_path=f"{current_dir}/ossutil64",
            create_oss_folder=False,
        )
        oss_data_downloader_sync.download(backup_dir="backup_dir")
        print(f"Copy files from {oss_data_folder} to {server_data_folder}")
        server_data_folder_file_list = os.listdir(server_data_folder)
        if len(server_data_folder_file_list) == 0:
            raise ValueError("No Data Copied")
        print(server_data_folder_file_list)

    if oss_weights_folder is not None:
        # 下载权重至服务器 server_weights_folder
        oss_weight_downloader_sync = OssSync(
            local_dir=server_weights_folder,
            oss_dir=oss_weights_folder,
            config_dir=current_dir,
            ossutil_path=f"{current_dir}/ossutil64",
            create_oss_folder=False,
        )
        oss_weight_downloader_sync.download(backup_dir="backup_dir")
        print(f"Copy files from {oss_weights_folder} to {server_weights_folder}")
        server_weights_folder_file_list = os.listdir(server_weights_folder)
        if len(server_weights_folder_file_list) == 0:
            raise ValueError("No Data Copied")
        print(server_weights_folder_file_list)

    return oss_uploader_callback, oss_expriment_folder_sync_uploader


def add_common_program_hparams(parent_parser, use_notebook):
    parser = ArgumentParser(parents=[parent_parser], add_help=False)
    parser.add_argument("--seed", type=int, default=2021)
    parser.add_argument("--log_level", type=str, default="info")
    parser.add_argument("--use_notebook", type=ast.literal_eval, default=use_notebook)
    parser.add_argument("-m", "--message", type=str, default="")
    parser.add_argument("--oss_enable", type=ast.literal_eval, default=False)
    parser.add_argument("--enable_progress_bar", type=ast.literal_eval, default=False)
    # personalization
    return parser


def add_common_data_hparams(parent_parser):
    parser = ArgumentParser(parents=[parent_parser], add_help=False)
    parser.add_argument("--num_workers", type=int, default=8)
    parser.add_argument("--pin_memory", type=ast.literal_eval, default=False)
    parser.add_argument("--persistent_workers", type=ast.literal_eval, default=True)
    parser.add_argument("--used_folds", nargs="+", default=0)
    parser.add_argument("--train_batch_size", type=int, default=10)  # [10 16p 12G], 32*8
    parser.add_argument("--valid_batch_size", type=int, default=20)  # [20 16p 12G], 32*8
    return parser


def add_common_model_hparams(parent_parser):
    parser = ArgumentParser(parents=[parent_parser], add_help=False)
    parser.add_argument("--model_name", type=str, default="no-name")
    # parser.add_argument("--num_outputs", type=int, default=1)
    return parser


def add_common_trainer_hparams(parent_parser):
    parser = ArgumentParser(parents=[parent_parser], add_help=False)
    parser.add_argument("--max_epochs", type=int, default=100)
    parser.add_argument("--gradient_clip_val", type=float, default=1)
    parser.add_argument("--gpus", nargs="+", default="0")
    parser.add_argument("--optimizer_info", type=str, default='adamw~{"lr":2e-5}')
    parser.add_argument("--attacker_info", type=str, default='constant~{"start_ratio": 0.5}')
    parser.add_argument(
        "--scheduler_info", type=str, default='get_cosine_schedule_with_warmup~{"warm_up_rate":0.1, "mode": "step"}'
    )
    parser.add_argument("--bwa_info", type=str, default='{"start_ratio":0.8, "weighted_ratio":0.5}')
    parser.add_argument("--r_drop_info", type=str, default='{"start_ratio":np.inf, "alpha": 0.3}')
    parser.add_argument("--precision", type=str, default="mixed")
    parser.add_argument("--num_eval_steps", type=int, default=0)
    # ModelCheckpoint
    parser.add_argument("--save_top_k", type=int, default=1)
    parser.add_argument("--monitor", type=str, default="valid_loss")
    parser.add_argument("--mode", type=str, default="min")
    # EarlyStopping
    parser.add_argument("--patience", type=int, default=5)
    return parser


def post_process_parser(parser, use_notebook, backup_code=True, print_info=True):
    # 适配notebook
    if use_notebook is True:
        hparams = parser.parse_args([])
    else:
        hparams = parser.parse_args()
    # TODO 适配多GPU,这里可能有问题，需要改造下
    if len(hparams.gpus[0]) == 1:
        hparams.gpus = [int(hparams.gpus[0])]
    else:
        hparams.gpus = [int(gpu) for gpu in hparams.gpus[0].split(",")]
    if isinstance(hparams.used_folds, int):
        hparams.used_folds = [hparams.used_folds]

    seed_reproducer(hparams.seed)
    if hparams.message == "":
        hparams.folder_name = get_current_time()[5:] + "-" + hparams.model_name
    else:
        hparams.folder_name = get_current_time()[5:] + "-" + hparams.model_name + "-" + hparams.message
    hparams.default_root_dir = os.path.join(ROOTFolder, os.path.join(hparams.dataset_name))
    hparams.experiment_location = f"{hparams.default_root_dir}/{hparams.folder_name}"
    print("Init hyper parameters Finish.")
    if print_info:
        print(pretty_json(hparams))
    if backup_code is True:
        backup_code_folder(hparams)
    return hparams


def get_trainer_parameters(hparams, print_info=True):
    trainer_parameters = {
        "experiment_location": hparams.experiment_location,
        "max_epochs": hparams.max_epochs,
        "num_eval_steps": hparams.num_eval_steps,
        "optimizer_info": hparams.optimizer_info,
        "scheduler_info": hparams.scheduler_info,
        "attacker_info": hparams.attacker_info,
        "r_drop_info": hparams.r_drop_info,
        "gradient_clip_val": hparams.gradient_clip_val,
        "gpus": hparams.gpus,
        "precision": hparams.precision,
    }
    if print_info:
        print(pretty_json(trainer_parameters))
    return trainer_parameters


class Scavenger:
    def __init__(self, hparams, oss_expriment_folder_sync_uploader, score=0) -> None:
        self.hparams = hparams
        self.score = round(score, 4)
        self.oss_expriment_folder_sync_uploader = oss_expriment_folder_sync_uploader
        self.used_folds = ",".join([str(i) for i in hparams.used_folds])

    def normal_clean(self):
        if self.hparams.oss_enable:
            # 利用产出的分值重命名oss folder
            oss_path_list = self.oss_expriment_folder_sync_uploader.oss_dir.split("/")
            oss_path_list[-1] = f"[Fold-{self.used_folds}-{self.score }]-" + oss_path_list[-1]
            self.oss_expriment_folder_sync_uploader.oss_dir = "/".join(oss_path_list)
            # 上传文件至OSS
            print("oss folder path: {self.oss_expriment_folder_sync_uploader.oss_dir}")
            self.oss_expriment_folder_sync_uploader.make_oss_dir()
            self.oss_expriment_folder_sync_uploader.upload()
        else:
            # 重命名本地文件
            oss_path_list = self.hparams.experiment_location.split("/")
            oss_path_list[-1] = f"[Fold-{self.used_folds}-{self.score}]-" + oss_path_list[-1]
            # 重命名本地文件
            print("local folder path: {oss_path_list}")
            os.system(f'mv {self.hparams.experiment_location} {"/".join(oss_path_list)}')

    def exception_clean(self):
        if self.hparams.oss_enable:
            # 利用产出的分值重命名oss folder
            oss_path_list = self.oss_expriment_folder_sync_uploader.oss_dir.split("/")
            oss_path_list[-1] = "fail-" + oss_path_list[-1]
            self.oss_expriment_folder_sync_uploader.oss_dir = "/".join(oss_path_list)
            print("oss folder path: {self.oss_expriment_folder_sync_uploader.oss_dir}")
            # 上传文件至OSS
            self.oss_expriment_folder_sync_uploader.make_oss_dir()
            self.oss_expriment_folder_sync_uploader.upload()
