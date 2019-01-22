# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/22'
"""

import unittest, sys, time, os, json, random
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
not_found_code = b.get_common("not_found_code")

api = b.get_api_v0_files_flush("api")


class ApiV0FilesFlush(unittest.TestCase):
    '''
    Flush a given path’s data to cluster.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    path	string	no	Path to flush. Default: ‘/’. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 or the following optional body:

    {
      "Message": "<string>"
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_err_uid_get(self):
        temp = "%s?uid=suxx" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_only_path_get(self):
        temp = "%s?path=/" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_uid_and_path_get(self):
        num = random.randint(0, 99999999999)
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)
        temp_api = "%s?arg=/%s&uid=%s" % (api, str(num),uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")
