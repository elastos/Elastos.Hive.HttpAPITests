# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/8'
"""

import unittest, sys, copy
sys.path.append("../")
import read_conf
from function.func import *
from function.ela_log import MyLog


log = MyLog.get_log()
logger = log.get_logger()

b = read_conf.ReadData()

normal_response_code = b.get_common("normal_response_code")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")
quiet_param_r = b.get_common("quiet_param_r")
quiet_param_e = b.get_common("quiet_param_e")

api = b.get_pins("api")

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")
pins_case = b.get_pins("200_code_cases")


class Pins(unittest.TestCase):
    '''
    list current status of pins in the cluster.

    METHOD:	GET Arguments
    Arguments	Type	Required	Description
    verbose	bool	no	Also write the hashes of non-broken pins.
    quiet	bool	no	Write just hashes of broken pins. default: no. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200.

    [
      {
        "Cid": "<string>",
        "peer_map":
        {
          "Peer ID String"
          {
            "cid": "<string>",
            "peer": "<string>",
            "peername": "<string>",
            "status": "<string>",
            "timestamp": "<string>",
            "error": "<string>"
          }
        }
      }
    ]
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        self.c = CaseMethod(api, "{}")
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case
    def test_normal_get(self):
        code, bcheck = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        self.assertEqual(bcheck, normal_response_code)

    @ConfigHttp.wrap_case
    def test_error_string_get(self):
        temp = copy.deepcopy(api)
        temp = temp + "s"
        code, bcheck = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        self.assertEqual(bcheck, not_found_code)

    @ConfigHttp.wrap_case
    def test_with_verbose(self):
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

    @ConfigHttp.wrap_case
    def test_with_quiet(self):
        quiet_cases_r = quiet_param_r.split(",")
        for quiet in quiet_cases_r:
            code, bcheck = self.c.get_check(quiet)
            self.assertEqual(code, normal_response_code)
            self.assertEqual(bcheck, 0)

        quiet_cases_e = quiet_param_e.split(",")
        for quiet in quiet_cases_e:
            code, bcheck = self.c.get_check(quiet)
            self.assertEqual(code, normal_response_code)
            self.assertEqual(bcheck, 0)

    @ConfigHttp.wrap_case
    def test_joint_arguments_get(self):
        p_c = self.f.list_conf_case(pins_case)
        for p in p_c:
            code, bcheck = self.c.get_check(p)
            self.assertEqual(code, normal_response_code)
            self.assertEqual(bcheck, 0)


# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Pins("test_with_correct_verbose"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)