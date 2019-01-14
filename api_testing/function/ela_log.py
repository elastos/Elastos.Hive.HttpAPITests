# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2018/12/29'
"""
import logging,os,sys
from datetime import datetime
import threading
sys.path.append("../")
import read_conf


class Log:
    def __init__(self):
        self.pro_dir = read_conf.pro_dir
        self.resultPath = os.path.join(self.pro_dir, "result")

        # create result file if it doesn't exist
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)
        # defined test result file name by localtime
        self.logPath = os.path.join(self.resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))

        # create test result file if it doesn't exist
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)

        # defined logger
        self.logger = logging.getLogger()

        # defined log level
        self.logger.setLevel(logging.INFO)

        # defined handler
        handler = logging.FileHandler(os.path.join(self.logPath, "output.log"))

        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # defined formatter
        handler.setFormatter(formatter)

        # add handler
        self.logger.addHandler(handler)

    def get_logger(self):
        logger_obj = logging.getLogger()
        fh = logging.FileHandler(os.path.join(self.logPath, "output.log"))
        fh.setLevel(logging.ERROR)
        ch = logging.StreamHandler()
        ch.setLevel(logging.CRITICAL)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger_obj.addHandler(fh)
        logger_obj.addHandler(ch)
        return logger_obj


class MyLog(Log):
    log = None
    mutex = threading.Lock()

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = MyLog()
            MyLog.mutex.release()

        return MyLog.log

a = MyLog.get_log()
print a.logPath
