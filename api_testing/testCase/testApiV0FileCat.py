# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/24'
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

api = b.get_api_v0_file_cat("api")


class ApiV0FileCat(unittest.TestCase):
    '''
    cat files content from the hive cluster

    METHOD:	GET/POST Arguments
    Argument	Type	Required	Description
    arg	string	yes	The path to the file(s) to be download from the cluster. Http Response
    Argument	Type	Required	Description
    http error	integer	yes	error code. On success, the call to this endpoint will return with 200 and the following body:
    http body	text/plain	no	This endpoint returns a text/plain response body (a TAR archive).
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_correct_arg_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        # Add the file.
        a1, b1 = self.f.run_cmd("curl -F file=@%s %s:%s/api/v0/add" % (fname, ipfs_master_api_baseurl,
                                                                       ipfs_master_api_port))
        logger.info(b1)

        Hash = json.loads(b1)["Hash"]
        temp_api = "%s?arg=%s" % (api, Hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")
        os.remove(fname)

    @Wrappers.wrap_case
    def test_err_arg_get(self):
        temp_api = "%s?arg=/xxxxxx" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")


    @Wrappers.wrap_case
    def test_unexist_arg_get(self):
        temp = self.f.random_str(44)
        un_exist_arg = "Qm%s" % temp
        logger.info("[Generate un-exist arg hash value]: %s" % un_exist_arg)

        temp_api = "%s?arg=%s" % (api, un_exist_arg)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")
