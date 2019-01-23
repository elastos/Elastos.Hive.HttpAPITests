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
api = b.get_api_v0_files_read("api")


class ApiV0FilesRead(unittest.TestCase):
    '''
    Read a file in a given path.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    path	string	yes	Path to file to be read.
    offset	integer	no	Byte offset to begin reading from.
    count	integer	no	Maximum number of bytes to read. HTTP Response
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
    def test_with_path_only_get(self):
        temp_api = "%s?path=/" % api
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_error_path_with_uid_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        pname = self.f.random_str()
        temp_api = "%s?path=/%s&uid=%s" % (api, pname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case
    def test_with_correct_path_with_correct_uid_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname,"a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        write_api = b.get_api_v0_files_write("api")
        temp_api = "%s?create=true&path=/%s&uid=%s" % (write_api, fname, uid)

        a1, b1 = self.f.run_cmd("curl -v -F file=@%s \"%s:%s%s\"" % (fname, ipfs_master_api_baseurl,
                                                                      ipfs_master_api_port, temp_api))
        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

        # Read the file
        temp_api = "%s?path=/%s&uid=%s" % (api, fname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(a1)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case
    def test_with_correct_path_with_correct_uid_with_other_arg_get(self):
        code_200_cases = b.get_api_v0_files_write("200_code_cases")
        p_c = self.f.list_conf_case(code_200_cases)

        for p in p_c:
            # Create new uid
            uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
            logger.info(uid)

            # Create random file name.
            fname = "%s" % self.f.random_str()
            logger.info(fname)
            with open(fname,"a") as f:
                f.write("This is file %s\n" % fname)
            f.close()

            write_api = b.get_api_v0_files_write("api")
            temp_api = "%s?create=true&path=/%s&uid=%s" % (write_api, fname, uid)

            a1, b1 = self.f.run_cmd("curl -v -F file=@%s \"%s:%s%s\"" % (fname, ipfs_master_api_baseurl,
                                                                          ipfs_master_api_port, temp_api))
            logger.info(a1)
            self.assertIn("200 OK", a1)
            os.remove(fname)

            # Read the file
            temp_api = "%s?path=/%s&uid=%s&%s" % (api, fname, uid, p)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(a1)
            logger.info(b1)
            self.assertEqual(b1, "200")

