# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2018/12/29'
"""

from function.func import *
import unittest
import HTMLTestRunner
import os
from function.ela_log import MyLog

caseListFile = "run_case_list.txt"
log = MyLog.get_log()
logger = log.get_logger()
caseList = []
# print log.resultPath


def set_case_list():
    fb = open(caseListFile)
    for value in fb.readlines():
        data = str(value)
        if data != '' and not data.startswith("#"):
            caseList.append(data.replace("\n", ""))
    fb.close()


def set_case_suite():
    set_case_list()
    test_suite = unittest.TestSuite()
    suite_model = []

    for case in caseList:
        case_file = os.path.join(readConfig.pro_dir, "testCase")
        print(case_file)
        case_name = case.split("/")[-1]
        print(case_name+".py")
        discover = unittest.defaultTestLoader.discover(case_file, pattern=case_name + '.py', top_level_dir=None)
        suite_model.append(discover)

    if len(suite_model) > 0:
        for suite in suite_model:
            for test_name in suite:
                test_suite.addTest(test_name)
    else:
        return None
    return test_suite


def run():
    try:
        suit = set_case_suite()
        if suit is not None:
            logger.info("********TEST START********")
            # logger.info("Test %s" % suit)
            fp = open("%s/report.html" % log.logPath, 'wb')
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='ELA IPFS-CLUSTER HTTP APIs Test Report',\
                                                   description='Run ipfs-cluster api test cases.')
            runner.run(suit)
        else:
            logger.info("Have no case to test.")
    except Exception as ex:
        logger.error(str(ex))
    finally:
        logger.info("*********TEST END*********")


if __name__ == '__main__':
    run()
