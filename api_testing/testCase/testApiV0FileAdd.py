# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/22'
"""

import unittest, sys, json, time, os
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

api = b.get_api_v0_file_add("api")
normal_response_body = b.get_api_v0_file_add("normal_response_body")


class ApiV0FileAdd(unittest.TestCase):
    '''
    Add a file or directory to cluster.

    METHOD:	GET/POST
    Argument	Type	Required	Description
    path	file	yes	The path to a file to be added to the cluster.
    recursive	bool	no	Add directory paths recursively. Default: “false”. Required: no.
    hidden	bool	no	Include files that are hidden. Only takes effect on recursive add. Default: “false”.
    pin	bool	no	Pin this object when adding. Default: “true”.
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_correct_arg_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        os.remove(fname)

        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_unexist_file_get(self):
        fname = "%s" % self.f.random_str()
        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))

        logger.info(a1)
        logger.info(b1)
        self.assertNotIn("200 OK", a1)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_recursive_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?recursive=1" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?recursive=0" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?recursive=xxx" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertNotIn("200 OK", a1)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_hidden_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?hidden=1" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?hidden=0" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?hidden=xxx" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertNotIn("200 OK", a1)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_pin_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?pin=1" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?pin=0" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?pin=xxx" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertNotIn("200 OK", a1)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_arg_string_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?hidde=1" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?resur=0" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?pinn=0" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_joint_arg_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?hidden=1&recursive=1" % (fname, ipfs_master_api_baseurl,
                                                                 ipfs_master_api_port, api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout 10 -m 10 -v -F file=@%s %s:%s%s?hidden=1&recursive=1&pin=0" % (fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        os.remove(fname)
