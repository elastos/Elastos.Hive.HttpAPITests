# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/19'
"""

import unittest, sys, json, time, os
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

api = b.get_api_v0_pin_add("api")
normal_response_body = b.get_api_v0_pin_add("normal_response_body")
# cases_200 = b.get_api_v0_uid_new("200_code_cases")


class ApiV0PinAdd(unittest.TestCase):
    '''

    Pin objects in the cluster

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    arg	string	yes	Path to object(s) to be pinned. Required: yes.
    recursive	bool	yes	Recursively pin the object linked to by the specified object(s). Default: “true”.
    progress	bool	no	Show progress. Default: "true" HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200.

    {
          "Pins": [
                  "<CID>"
          ],
          "Progress": "<int>"
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
        self.assertEqual(b1, internal_server_error)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_arg_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open("temp.txt","a") as f:
            f.write("[%s] [%s] [%s]." % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()

        a1, x1 = self.f.run_cmd('curl --connect-timeout 10 -m 10 -F "file=@temp.txt" %s:%s/api/v0/add' % (ipfs_master_api_baseurl,
                                                                               ipfs_master_api_port))
        logger.info(x1)
        hash = json.loads(x1)["Hash"]
        temp = "%s?arg=%s" % (api, hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_inexistent_arg_get(self):
        test_v = "QmTEmptemtemtemtmetmetmetmetmemtemtmetmetmetmp"
        temp = "%s?arg=%s" % (api, test_v)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_error_arg_get(self):
        test_v = "xxx"
        temp = "%s?arg=%s" % (api, test_v)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, internal_server_error)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_recursive_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open("temp.txt","w") as f:
            f.write("[%s] [%s] [%s].\n" % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()
        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -F file=@temp.txt %s:%s/api/v0/add" % (ipfs_master_api_baseurl,
                                                                             ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s&recursive=0" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)
        temp = "%s?arg=%s&recursive=false" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_hidden_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open("temp.txt", "w") as f:
            f.write("[%s] [%s] [%s].\n" % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -F file=@temp.txt %s:%s/api/v0/add" % (ipfs_master_api_baseurl,
                                                                             ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s&hidden=1" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)
        temp = "%s?arg=%s&hidden=true" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_joint_param_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open("temp.txt", "w") as f:
            f.write("[%s] [%s] [%s].\n" % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()
        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -F file=@temp.txt %s:%s/api/v0/add" % (ipfs_master_api_baseurl,
                                                                             ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s&recursive=1&hidden=1" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_joint_err_param_get(self):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open("temp.txt", "w") as f:
            f.write("[%s] [%s] [%s].\n" % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
        f.close()
        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -F file=@temp.txt %s:%s/api/v0/add" % (ipfs_master_api_baseurl,
                                                                             ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s&recursive=directxxx&hidden=11" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)


