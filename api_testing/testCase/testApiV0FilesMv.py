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
api = b.get_api_v0_files_mv("api")


class ApiV0FilesMv(unittest.TestCase):
    '''
    Move files.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    source	string	yes	Source file to move.
    dest	string	yes	Destination path for file to be moved to. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 or the following optional body:

    {
      "Message": "<string>"
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        self.c = CaseMethod(api, {}, "ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_uid_only_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        temp_api = "%s?uid=%s" % (api, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_source_only_get(self):
        temp_api = "%s?source=/" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_dest_only_get(self):
        temp_api = "%s?dest=/" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_dest_and_source_only_get(self):
        temp_api = "%s?dest=/&source=/" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_all_arg_with_err_value_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create error dest.
        dpath = self.f.random_str()

        temp_api = "%s?uid=%s&source=/&dest=/%s" % (api, uid, dpath)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_all_arg_with_correct_value_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create source and dest.
        dir1 = self.f.random_str()
        dir2 = self.f.random_str()

        # Make dir.
        mkdir_api = b.get_api_v0_files_mkdir("api")
        temp_api = "%s?uid=%s&path=/%s" % (mkdir_api, uid, dir1)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

        temp_api = "%s?uid=%s&path=/%s" % (mkdir_api, uid, dir2)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

        # Mv
        temp_api = "%s?uid=%s&source=/%s&dest=/%s" % (api, uid, dir1, dir2)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")