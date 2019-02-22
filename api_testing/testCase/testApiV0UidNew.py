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
curl_connect_timeout = a.get_ipfs_cluster("curl_connect_timeout")
curl_max_timeout = a.get_ipfs_cluster("curl_max_timeout")

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
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_no_argument_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_uid_changed(self):
        a1, b1 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        a2, b2 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b2)
        self.assertNotEqual(b1, b2)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_get_with_str(self):
        p_c = self.f.list_conf_case(cases_200)
        for p in p_c:
            api_temp = "%s?%s" % (api, p)
            a1, code = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
            logger.info(code)
            self.assertEqual(code, "200")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_func_newid_check_oldid_dir_tree(self):
        # Create a new id
        uid = self.f.get_new_id2(ipfs_master_api_baseurl, ipfs_master_api_port, curl_connect_timeout,
                                 curl_max_timeout)
        logger.info(uid)

        # Check the uid's dir_tree
        api_ls = b.get_api_v0_files_ls("api")
        temp_api = "%s?uid=%s" % (api_ls, uid)
        dir_tree = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api, curl_connect_timeout,
                                        curl_max_timeout)

        # Use the uid create a directory.
        pname = self.f.random_str()
        api_mkdir = b.get_api_v0_files_mkdir("api")
        temp_api = "%s?path=/%s&uid=%s" % (api_mkdir, pname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api, curl_connect_timeout,
                                      curl_max_timeout)
        logger.info(b1)
        self.assertEqual(b1, "200")

        # Check the uid's dir_tree
        temp_api = "%s?uid=%s" % (api_ls, uid)
        dir_tree_2 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api, curl_connect_timeout,
                                          curl_max_timeout)
        logger.info("COMPARE:")
        logger.info(dir_tree_2)
        logger.info(dir_tree)
        logger.info("")
        # self.assertEqual(dir_tree_2, dir_tree)

        # Create a new id
        uid2 = self.f.get_new_id2(ipfs_master_api_baseurl, ipfs_master_api_port, curl_connect_timeout,
                                  curl_max_timeout)
        logger.info(uid2)

        # Check the uid2's dir_tree
        temp_api = "%s?uid=%s" % (api_ls, uid2)
        dir_tree_3 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api, curl_connect_timeout,
                                          curl_max_timeout)

        logger.info("COMPARE:")
        logger.info(dir_tree_3)
        logger.info(dir_tree)
        logger.info("")
        # self.assertEqual(dir_tree_3, dir_tree)

        temp_api = "%s?uid=%s&path=/%s" % (api_ls, uid2, pname)
        dir_tree_4 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api, curl_connect_timeout,
                                          curl_max_timeout)
        logger.info("COMPARE:")
        logger.info(dir_tree_4)
        logger.info(dir_tree)
        logger.info("")
        # self.assertEqual(dir_tree_4, dir_tree)
