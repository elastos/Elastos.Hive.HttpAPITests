# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/4'
"""

import unittest,sys
sys.path.append("../")
import read_conf
from function.func import *
from function.ela_log import MyLog

log = MyLog.get_log()
logger = log.get_logger()

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

b = read_conf.ReadData()
api = b.get_id("api")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")

normal_response_body = b.get_id("normal_response_body")


class Id(unittest.TestCase):
    '''
    Show the cluster peers and its daemon information

    Arguments

    Arguments	Type	Required	Description
    verbose	bool	no	display all extra information.
    HTTP Response

    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
          "id": "<NodeId>",
          "peers": [
                  "/ip4/104.236.176.52/tcp/4001",
                  "/ip4/104.236.176.52/tcp/4001"
          ]
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        self.c = CaseMethod(api, normal_response_body)
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case
    def test_normal_get(self):
        code, bcheck = self.c.get_check()
        self.assertEqual(code, "200")
        self.assertEqual(bcheck, 0)

    @ConfigHttp.wrap_case
    def test_error_api_get(self):
        f = ConfigHttp()
        temp_api = api * 2
        o, e = f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(o)
        logger.info(e)
        self.assertEqual(e, "404")

    @ConfigHttp.wrap_case
    def test_normal_post_405(self):
        # Check code 404
        o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(o)
        logger.info(e)
        self.assertEqual(e, "405")

    @ConfigHttp.wrap_case
    def test_with_verbose_get(self):
        verbose_cases_r = verbose_param_r.split(",")
        for verbose in verbose_cases_r:
            code, bcheck = self.c.get_check(verbose)
            self.assertEqual(code, "200")
            self.assertEqual(bcheck, 0)

        verbose_cases_e = verbose_param_e.split(",")
        for verbose in verbose_cases_e:
            code, bcheck = self.c.get_check(verbose)
            self.assertEqual(code, "200")
            self.assertEqual(bcheck, 0)

    @ConfigHttp.wrap_case
    def test_with_error_param_get(self):
        code, bcheck = self.c.get_check("verbos=1")
        self.assertEqual(code, "200")
        self.assertEqual(bcheck, 0)

