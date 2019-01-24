# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/19'
"""

import unittest, sys
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

api = b.get_api_v0_uid_new("api")
normal_response_body = b.get_api_v0_uid_new("normal_response_body")
cases_200 = b.get_api_v0_uid_new("200_code_cases")


class ApiV0UidNew(unittest.TestCase):
    '''

        Create a unique UID and peer ID pair from Hive cluster.
        The UID can be used to identify endpoints in communication， the PeerID is a virtual IPFS peer ID.

        {
            "UID": "<string>",
            "PeerID": "<string>"
        }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        self.c = CaseMethod(api, normal_response_body, "ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case
    def test_no_argument_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case
    def test_uid_changed(self):
        a1, b1 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        a2, b2 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b2)
        self.assertNotEqual(b1, b2)

    @Wrappers.wrap_case
    def test_get_with_str(self):
        p_c = self.f.list_conf_case(cases_200)
        for p in p_c:
            api_temp = "%s?%s" % (api, p)
            a1, code = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
            logger.info(code)
            self.assertEqual(code, "200")



