# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/21'
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
normal_response_code = b.get_common("normal_response_code")
abnormal_response_code = b.get_common("abnormal_response_code")
internal_server_error = b.get_common("internal_server_error")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")
quiet_param_r = b.get_common("quiet_param_r")
quiet_param_e = b.get_common("quiet_param_e")

api = b.get_api_v0_pin_ls("api")
normal_response_body = b.get_api_v0_pin_ls("normal_response_body")
types = b.get_api_v0_pin_ls("type")
cases_200 = b.get_api_v0_pin_ls("200_code_cases")


class ApiV0PinLs(unittest.TestCase):
    '''
    List objects that pinned to the cluster.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    arg	string	yes	Path to object(s) to be pinned. Required: yes.
    type	string	no	The type of pinned keys to list. Can be “direct”, “indirect”, “recursive”, or “all”. Default: “all”.
    quiet	bool	no	Write just hashes of objects. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200.

    {
          "Keys":
          {
                  "<Object CID>":
                  {
                    "Type": "<string>"
                  }
          }
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        self.c = CaseMethod(api, normal_response_body, "ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_arg_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open("temp.txt", "a") as f:
            f.write("[%s] [%s] [%s]." % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -F file=@temp.txt %s:%s/api/v0/add" % (ipfs_master_api_baseurl,
                                                                             ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_quiet_get(self):
        quiet_cases_r = quiet_param_r.split(",")
        for q in quiet_cases_r:
            temp_api = api + "?" + q
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_type_get(self):
        type_l = types.split(",")
        for type in type_l:
            temp_api = api + "?" + type
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_joint_parm_get(self):
        p_c = self.f.list_conf_case(cases_200)
        for p in p_c:
            api_temp = "%s?%s" % (api, p)
            a1, code = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
            logger.info(code)
            self.assertEqual(code, normal_response_code)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ApiV0PinLs("test_normal_get"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

