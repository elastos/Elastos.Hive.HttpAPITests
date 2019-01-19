# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/19'
"""

import unittest, sys, json
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

api = b.get_api_v0_file_pin_add("api")
normal_response_body = b.get_api_v0_file_pin_add("normal_response_body")
# cases_200 = b.get_api_v0_uid_new("200_code_cases")


class ApiV0FilePinAdd(unittest.TestCase):
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

    @Wrappers.wrap_case
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, internal_server_error)

    @Wrappers.wrap_case
    def test_with_arg_get(self):
        a1, b1 = self.f.curl_cmd("curl -F file=@all_cases.txt %s:%s/api/v0/add" % (ipfs_master_api_baseurl,ipfs_master_api_port))
        logger.info(b1)
        Hash = json.loads(b1)["Hash"]
        temp = "%s?arg=%s" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp)
        logger.info(b1)
        self.assertEqual(b1, normal_response_code)