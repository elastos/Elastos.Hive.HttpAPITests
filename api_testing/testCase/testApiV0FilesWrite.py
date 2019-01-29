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
api = b.get_api_v0_files_write("api")
code_200_cases = b.get_api_v0_files_write("200_code_cases")


class ApiV0FilesWrite(unittest.TestCase):
    '''
    Write to a mutable file in a given filesystem.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    path	string	yes	Path to write to.
    file	file	yes	Data to write.
    offset	integer	no	Byte offset to begin writing at. Default: 0.
    create	bool	no	Create the file if it does not exist.
    truncate	bool	yes	Truncate the file to size zero before writing.
    count	int	no	Maximum number of bytes to read. Request Body
    Argument “data” is of file type. This endpoint expects a file in the body of the request as ‘multipart/form-data’. HTTP Response
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
    def test_only_uid_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        temp_api = api + "?uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_err_uid_only_get(self):
        temp_api = api + "?uid=xxxxxxx"
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_uid_and_path_without_file_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        temp_api = api + "?create=true&path=/xx.txt&uid=" + uid
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_uid_path_and_file_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname,"a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        temp_api = "%s?create=true&path=/%s&uid=%s" % (api, fname, uid)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s \"%s:%s%s\"" % (fname, ipfs_master_api_baseurl,
                                                                      ipfs_master_api_port, temp_api))
        logger.info(a1)
        self.assertIn("200 OK", a1)
        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_other_arg_and_correct_value_get(self):
        cases = code_200_cases.split(",")
        for c_api in cases:
            # Create new uid
            uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
            logger.info(uid)

            # Create random file name.
            fname = "%s" % self.f.random_str()
            logger.info(fname)
            with open(fname, "a") as f:
                f.write("This is file %s\n" % fname)
            f.close()

            temp_api = "%s?create=true&path=/%s&uid=%s&%s" % (api, fname, uid, c_api)

            a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s \"%s:%s%s\"" % (fname, ipfs_master_api_baseurl,
                                                                         ipfs_master_api_port, temp_api))
            logger.info(a1)
            self.assertIn("200 OK", a1)
            os.remove(fname)

