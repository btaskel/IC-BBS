import logging
import os
from datetime import datetime

def initLogging(level=logging.INFO):
    if level == 5:
        level = logging.DEBUG
    elif level == 4:
        level = logging.INFO
    elif level == 3:
        level = logging.WARNING
    elif level == 2:
        level = logging.ERROR
    elif level == 1:
        level = logging.CRITICAL
    else:
        level = logging.INFO

    # 创建一个文件夹logs在当前目录下
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 获取当前日期作为日志文件名
    log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
    log_filepath = os.path.join('logs', log_filename)

    logging.basicConfig(
        filename='debug.log',
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S '
    )

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(log_filepath)
    fh.setLevel(level)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger = logging.getLogger()
    logger.addHandler(fh)
    logger.addHandler(ch)