# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/23'
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
api = b.get_api_v0_files_stat("api")
normal_response_body = b.get_api_v0_files_stat("normal_response_body")


class ApiV0FilesStat(unittest.TestCase):
    '''
    Display file status.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    path	string	yes	Path to node to stat.
    format	string	no	Print statistics in given format. Allowed tokens: . Conflicts with other format options. Default: Size: CumulativeSize: ChildBlocks: Type: . Default: “ Size: CumulativeSize: ChildBlocks: Type: ”.
    hash	string	no	Print only hash. Implies ‘–format=’. Conflicts with other format options. Required: no.
    with-local	string	no	Compute the amount of the dag that is local, and if possible the total size. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
          "Hash": "<string>",
          "Size": "<uint64>",
          "CumulativeSize": "<uint64>",
          "Blocks": "<int>",
          "Type": "<string>",
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
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_correct_uid_with_error_path_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        err_path = "/%s" % self.f.random_str()

        temp_api = api + "?path=" + err_path + "&uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_correct_uid_with_correct_path_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        temp_api = api + "?path=/&uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_correct_path_without_uid_get(self):
        temp_api = api + "?path=/"
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_format_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        temp_api = api + "?format=xxx&path=/&uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_hash_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        temp_api = api + "?hash=xxx&path=/&uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")