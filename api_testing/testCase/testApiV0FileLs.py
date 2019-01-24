# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/22'
"""

import unittest, sys, time, os, json
sys.path.append("../")
import read_conf
from function.func import *
from function.ela_log import MyLog

log = MyLog.get_log()
logger = log.get_logger()

a = read_conf.ReadConfig()
b = read_conf.ReadData()

ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_endpoint_port")

api = b.get_api_v0_file_ls("api")
normal_response_body = b.get_api_v0_file_ls("normal_response_body")


class ApiV0FileLs(unittest.TestCase):
    '''
    List directory contents for Unix filesystem objects.

    METHOD:	GET/POST Arguments
    Argument	Type	Required	Description
    path	file	yes	The path to the IPFS object(s) to list links from. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
          "Arguments": {
                  "<string>": "<string>"
          },
          "Objects": {
                  "<string>": {
                          "Hash": "<string>",
                          "Size": "<uint64>",
                          "Type": "<string>",
                          "Links": [{
                                  "Name": "<string>",
                                  "Hash": "<string>",
                                  "Size": "<uint64>",
                                  "Type": "<string>"
                          }]
                  }
          }
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        self.c = CaseMethod(api, normal_response_body, "ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "400")

    @Wrappers.wrap_case
    def test_err_arg_value_get(self):
        temp = "%s?arg=xxxxxx" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "400")

    @Wrappers.wrap_case
    def test_correct_value_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        fname = self.f.random_str()
        with open(fname, "w") as f:
            f.write("[%s] [%s] [%s].\n" % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()

        a1, b1 = self.f.run_cmd("curl -F file=@%s %s:%s/api/v0/add" % (fname, ipfs_master_api_baseurl,
                                                                       ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, "200")

