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
normal_response_code = b.get_common("normal_response_code")
abnormal_response_code = b.get_common("abnormal_response_code")
internal_server_error = b.get_common("internal_server_error")
not_found_code = b.get_common("not_found_code")

api = b.get_api_v0_files_ls("api")
normal_response_body = b.get_api_v0_files_ls("normal_response_body")


class ApiV0FilesMkdir(unittest.TestCase):
    '''
    List directories in the private mutable namespace.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    path	string	no	Path to show listing for. Defaults to ‘/’. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
            "Entries": [{
                    "Name": "<string>",
                    "Type": "<int>",
                    "Size": "<int64>",
                    "Hash": "<string>"
            }]
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
        self.assertEqual(b1, internal_server_error)

    @Wrappers.wrap_case
    def test_with_path_with_uid_get(self):
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)
        temp_api = "%s?arg=/&uid=%s" % (api, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case
    def test_only_with_uid_get(self):
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)
        temp_api = "%s?uid=%s" % (api, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case
    def test_only_with_err_uid_get(self):
        uid = "suxx"
        temp_api = "%s?uid=%s" % (api, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, internal_server_error)

    @Wrappers.wrap_case
    def test_only_with_path_get(self):
        temp_api = "%s?path=/" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, internal_server_error)


