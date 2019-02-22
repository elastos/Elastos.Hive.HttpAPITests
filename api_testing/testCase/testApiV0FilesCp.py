# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/22'
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
curl_connect_timeout = a.get_ipfs_cluster("curl_connect_timeout")
curl_max_timeout = a.get_ipfs_cluster("curl_max_timeout")

api = b.get_api_v0_files_cp("api")
write_api = b.get_api_v0_files_write("api")
mkdir_api = b.get_api_v0_files_mkdir("api")


class ApiV0FilesCp(unittest.TestCase):
    '''
    Copy files among clusters.
    
    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    source	string	no	Source object to copy.
    dest	string	no	Destination to copy object to. HTTP Response
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
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        err_path = "/%s" % self.f.random_str()

        temp_api = api + "?uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_correct_args_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        temp_api = "%s?create=true&path=/%s&uid=%s" % (write_api, fname, uid)
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s&pin=1\"" % (
            curl_connect_timeout,
            curl_max_timeout,
            fname,
            ipfs_master_api_baseurl,
            ipfs_master_api_port,
            temp_api))

        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

        # Create random new path
        npath = "/%s" % self.f.random_str()
        temp_api = "%s?uid=%s&path=%s" % (mkdir_api, uid, npath)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s\"" % (
            curl_connect_timeout,
            curl_max_timeout,
            ipfs_master_api_baseurl,
            ipfs_master_api_port,
            temp_api))

        logger.info(a1)
        self.assertIn("200 OK", a1)

        # cp
        temp_api = "%s?uid=%s&source=/&dest=%s" % (api, uid, npath)
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s\"" % (
            curl_connect_timeout,
            curl_max_timeout,
            ipfs_master_api_baseurl,
            ipfs_master_api_port,
            temp_api))

        logger.info(a1)
        self.assertIn("200 OK", a1)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_source_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        temp_api = "%s?create=true&path=/%s&uid=%s" % (write_api, fname, uid)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s&pin=1\"" % (
            curl_connect_timeout,
            curl_max_timeout,
            fname,
            ipfs_master_api_baseurl,
            ipfs_master_api_port,
            temp_api))

        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

        # Create randon new path
        npath = "/%s" % self.f.random_str()
        temp_api = "%s?uid=%s" % (mkdir_api, npath)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

        # cp
        temp_api = "%s?uid=%s&source=/xxx&dest=%s" % (api, uid, npath)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_source_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        temp_api = "%s?create=true&path=/%s&uid=%s" % (write_api, fname, uid)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s&pin=1\"" % (
            curl_connect_timeout,
            curl_max_timeout,
            fname,
            ipfs_master_api_baseurl,
            ipfs_master_api_port,
            temp_api))

        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

        # cp
        temp_api = "%s?uid=%s&source=/&dest=/xxxx" % (api, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

