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

api = b.get_api_v0_uid_login("api")
normal_response_body = b.get_api_v0_uid_login("normal_response_body")


class ApiV0UidLogin(unittest.TestCase):
    '''

    Log in to Hive Cluster using the UID you created earlier.

    Arguments
    Arguments	Type	Required	Description
    uid	string	yes	The UID you created earlier.
    METHOD:	GET/POST HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
      "UID": "<string>",
      "OldUID": "<string>",
      "PeerID": "<string>"
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_without_uid_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_uid_get(self):
        api_temp = "%s?uid=xxxxx" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_arg_get(self):
        api_temp = "%s?xxxxx" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_normal_get(self):
         api_new = b.get_api_v0_uid_new("api")
         a1, b1 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api_new)
         temp = json.loads(b1)
         uid = temp["UID"]
         logger.info(uid)
         api_temp = "%s?uid=%s" % (api, str(uid))
         a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
         logger.info(b1)
         self.assertEqual(b1, "200")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_renew_uid_check_dir_tree_get(self):
        # Create a new id
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Check the uid's dir_tree
        api_ls = b.get_api_v0_files_ls("api")
        temp_api = "%s?uid=%s" % (api_ls, uid)
        dir_tree = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)

        # Use the uid create a directory.
        pname = self.f.random_str()
        api_mkdir = b.get_api_v0_files_mkdir("api")
        temp_api = "%s?path=/%s&uid=%s" % (api_mkdir, pname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

        # Renew a uid
        a1, b1 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        temp = json.loads(b1)
        uid = temp["UID"]
        logger.info(uid)
        api_temp = "%s?uid=%s" % (api, str(uid))
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
        logger.info(b1)
        self.assertEqual(b1, "200")

        a1, b1 = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api_temp)
        logger.info(b1)

