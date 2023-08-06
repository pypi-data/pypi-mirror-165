"""
 Author: yican.yc
 Date: 2022-08-23 19:24:49
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:24:49
"""
import logging
import os
import time
from datetime import datetime
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from functools import wraps

level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.warning,
    "error": logging.ERROR,
    "critircal": logging.CRITICAL,
}


# ==============================================================================================================
# Logging
# ==============================================================================================================
class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        datefmt = "%Y-%m-%d %H:%M:%S"
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt)
        return formatter.format(record)


def init_logger(logger_name="terminal", log_dir=None, notebook=False):
    """日志模块
    Reference: https://juejin.im/post/5bc2bd3a5188255c94465d31
    日志器初始化
    日志模块功能:
        1. 日志同时打印到到屏幕和文件
        2. 默认保留近一周的日志文件
    日志等级:
        NOTSET（0）、DEBUG（10）、INFO（20）、WARNING（30）、ERROR（40）、CRITICAL（50）
    如果设定等级为10, 则只会打印10以上的信息

    Parameters
    ----------
    logger_name : str
        日志文件名
    log_dir : str
        日志保存的目录

    Returns
    -------
    RootLogger
        Python日志实例
    """

    # 若多处定义Logger，根据logger_name确保日志器的唯一性
    if logger_name not in Logger.manager.loggerDict:
        logging.root.handlers.clear()
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # 定义日志信息格式
        datefmt = "%Y-%m-%d %H:%M:%S"
        if notebook is True:
            format_str = "[%(asctime)s] [%(lineno)4s] : %(levelname)s  %(message)s"
        else:
            format_str = "[%(asctime)s] %(filename)s[%(lineno)4s] : %(levelname)s  %(message)s"
        formatter = logging.Formatter(format_str, datefmt)

        # 日志等级INFO以上输出到屏幕
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_dir is not None:
            os.makedirs(log_dir, exist_ok=True)
            # 日志等级INFO以上输出到{logger_name}.log文件
            file_info_handler = TimedRotatingFileHandler(
                filename=os.path.join(log_dir, "%s.log" % logger_name), when="D", backupCount=7
            )
            file_info_handler.setFormatter(formatter)
            file_info_handler.setLevel(logging.INFO)
            logger.addHandler(file_info_handler)

    logger = logging.getLogger(logger_name)

    return logger


def set_logger_level(logger, level="info"):
    """设置logging和logger下所有handlers的level,

    Parameters
    ----------
    logger : python logger对象
        待修改level的logger
    level : str, optional, by default "info"
        "debug": logging.DEBUG
        "info": logging.INFO
        "warning": logging.warning
        "error": logging.ERROR
        "critircal": logging.CRITICAL
    """
    logger.setLevel(level_map[level])
    for h in logger.handlers:
        h.setLevel(level_map[level])


def log_start_time(message):
    global st_time
    st_time = time.time()
    print(
        """
# =================================================================================
# START !!! {}    PID: {}    Time: {}
# =================================================================================
""".format(
            message, os.getpid(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    #    send_line(f'START {fname}  time: {elapsed_minute():.2f}min')

    return


def log_end_time(message):
    print(
        """
# =================================================================================
# SUCCESS !!! {}  Total Time: {} seconds
# =================================================================================
""".format(
            message, int(time.time() - st_time)
        )
    )
    return


def timer(func):
    """Decorator for measuring time elapsed of function.
    @wraps can remove the conflict with multiprocess.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        print("{} : {} seconds".format(func.__name__, int(time.time() - start_time)))
        return res

    return wrapper
