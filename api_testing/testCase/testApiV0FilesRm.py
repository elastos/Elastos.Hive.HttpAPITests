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
api = b.get_api_v0_files_rm("api")


class ApiV0FilesRm(unittest.TestCase):
    '''
    Remove a file.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    path	string	yes	File to remove.
    recursive	bool	no	Recursively remove directories. default: false HTTP Response
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

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_rm_dir_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        dirname = "%s" % self.f.random_str()
        mk_api = b.get_api_v0_files_mkdir("api")
        temp_api = "%s?path=/%s&uid=%s" % (mk_api, dirname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

        # Try rm a directory.
        temp_api = "%s?path=/%s&uid=%s" % (api, dirname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_rm_un_exist_file_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        fname = "%s" % self.f.random_str()
        temp_api = "%s?path=/%s&uid=%s" % (api, fname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_rm_file_with_correct_argument_get(self):
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

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s \"%s:%s%s\"" % (fname, ipfs_master_api_baseurl,
                                                                      ipfs_master_api_port, temp_api))
        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

        # Rm the file
        temp_api = "%s?path=/%s&uid=%s" % (api, fname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_rm_file_with_recursive_argument_get(self):
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

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s \"%s:%s%s\"" % (fname, ipfs_master_api_baseurl,
                                                                      ipfs_master_api_port, temp_api))
        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

        # Rm the file
        temp_api = "%s?path=/%s&uid=%s&recursive=1" % (api, fname, uid)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")
