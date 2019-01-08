# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/7'
"""

import read_conf
import unittest,sys,json
sys.path.append("../")
from function.func import *
from function.ela_log import MyLog


log = MyLog.get_log()
logger = log.get_logger()

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

b = read_conf.ReadData()

normal_response_code = b.get_common("normal_response_code")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")

api = b.get_peers("api")
normal_response_body = b.get_peers("normal_response_body")



class Peers(unittest.TestCase):
    '''
    List the cluster servers with open connections.

    METHOD:	GET Arguments
    Arguments	Type	Required	Description
    verbose	bool	no	display all extra information. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
          "data": [
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
        self.assertEqual(code, normal_response_code)
        self.assertEqual(bcheck, 0)

    @ConfigHttp.wrap_case
    def test_with_verbose_get(self):
        verbose_cases_r = verbose_param_r.split(",")
        for verbose in verbose_cases_r:
            code, bcheck = self.c.get_check(verbose)
            self.assertEqual(code, normal_response_code)
            self.assertEqual(bcheck, 0)

        verbose_cases_e = verbose_param_e.split(",")
        for verbose in verbose_cases_e:
            code, bcheck = self.c.get_check(verbose)
            self.assertEqual(code, normal_response_code)
            self.assertEqual(bcheck, 0)


# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Peers("test_with_verbose_get"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)

