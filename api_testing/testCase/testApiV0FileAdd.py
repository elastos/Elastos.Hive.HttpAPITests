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
curl_connect_timeout = a.get_ipfs_cluster("curl_connect_timeout")
curl_max_timeout = a.get_ipfs_cluster("curl_max_timeout")

api = b.get_api_v0_file_add("api")
normal_response_body = b.get_api_v0_file_add("normal_response_body")

loop = b.get_api_v0_file_add("loop")
ipfs_slave_string = a.get_ipfs_cluster("ipfs_slaves")
ipfs_slave_l = list(eval(ipfs_slave_string))


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

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s\"" % (curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        os.remove(fname)

        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_unexist_file_get(self):
        fname = "%s" % self.f.random_str()
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s\"" % (curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))

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
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?recursive=1\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?recursive=0\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?recursive=xxx\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
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

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?hidden=1\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?hidden=0\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?hidden=xxx\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
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

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=1\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=0\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=xxx\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_arg_string_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?hidde=1\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?resur=0\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pinnn=0\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_joint_arg_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info("Create %s." % fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?hidden=1&recursive=1\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?hidden=1&recursive=1&pin=0\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)
        x = self.f.check_body(json.loads(b1), json.loads(normal_response_body))
        self.assertEqual(x, 0)

        os.remove(fname)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_node1_add_node2_cat_arg_get(self):
        # Create random file name.
        fname = "%s" % self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s." % fname)
        f.close()

        # Add the file.
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=1\"" % (
                                                                                            curl_connect_timeout,
                                                                                            curl_max_timeout,
                                                                                            fname,
                                                                                            ipfs_master_api_baseurl,
                                                                                            ipfs_master_api_port,
                                                                                            api))
        logger.info(a1)
        logger.info(b1)
        os.remove(fname)
        self.assertIn("200 OK", a1)

        # Get hash value.
        Hash = json.loads(b1)["Hash"]

        # Cat the file on another node.
        ipfs_slave_api_baseurl_1 = a.get_ipfs_cluster("ipfs_slave_api_baseurl_1")
        ipfs_slave_api_endpoint_port_1 = a.get_ipfs_cluster("ipfs_slave_api_endpoint_port_1")

        api_cat = b.get_api_v0_file_cat("api")
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s?arg=%s\"" % (
                                                                                curl_connect_timeout,
                                                                                curl_max_timeout,
                                                                                ipfs_slave_api_baseurl_1,
                                                                                ipfs_slave_api_endpoint_port_1,
                                                                                api_cat, Hash))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_files_add_get(self):
        files_num = b.get_api_v0_file_add("files_num")
        for i in range(0, int(files_num)):
            # Create random file name.
            fname = "%s_%s" % (str(i), self.f.random_str())
            logger.info(fname)
            current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            with open(fname, "w") as f:
                f.write("[%s] [%s] [%s].\n" % (current, os.path.basename(__file__), sys._getframe().f_code.co_name))
            f.close()

            # Add the file.
            a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=1\"" % (
                                                                                                curl_connect_timeout,
                                                                                                curl_max_timeout,
                                                                                                fname,
                                                                                                ipfs_master_api_baseurl,
                                                                                                ipfs_master_api_port,
                                                                                                api))
            logger.info(a1)
            logger.info(b1)
            os.remove(fname)
            self.assertIn("200 OK", a1)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_files_add_and_cat_each_node_get(self):
        for i in range(0, int(loop)):
            # Create random file name.
            fname = "%s_%s" % (str(i), self.f.random_str())
            logger.info(fname)
            current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            with open(fname, "w") as f:
                f.write("[%s] [%s] [%s].\n This file should be cat by other nodes." % (
                    current, os.path.basename(__file__), sys._getframe().f_code.co_name))
            f.close()

            # Add the file.
            a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=1\"" % (
                                                                                                curl_connect_timeout,
                                                                                                curl_max_timeout,
                                                                                                fname,
                                                                                                ipfs_master_api_baseurl,
                                                                                                ipfs_master_api_port,
                                                                                                api))
            logger.info(a1)
            logger.info(b1)
            os.remove(fname)
            self.assertIn("200 OK", a1)

            # Get hash value.
            Hash = json.loads(b1)["Hash"]

            # Cat on each node.
            api_cat = b.get_api_v0_file_cat("api")
            for nod in ipfs_slave_l:
                n_url = nod["url"]
                n_eport = nod["eport"]

                a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s?arg=%s\"" % (
                                                                                        curl_connect_timeout,
                                                                                        curl_max_timeout,
                                                                                        n_url,
                                                                                        n_eport,
                                                                                        api_cat, Hash))
                logger.info(a1)
                logger.info(b1)

                self.assertIn("200 OK", a1)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_each_node_add_and_other_cat_get(self):
        ipfs_slave_string = a.get_ipfs_cluster("ipfs_slaves")
        ipfs_slave_l = list(eval(ipfs_slave_string))

        for i in range(0, int(loop)):
            logger.info("-------------")
            logger.info("---loop %s---" % i)
            logger.info("-------------\n")
            # Create random file name.
            fname = "%s_%s" % (str(i), self.f.random_str())
            logger.info(fname)
            current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            with open(fname, "w") as f:
                f.write("[%s] [%s] [%s].\n This file should be cat by other nodes." % (
                    current, os.path.basename(__file__), sys._getframe().f_code.co_name))
            f.close()

            # Add the file.
            a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=1\"" % (
                                                                                                curl_connect_timeout,
                                                                                                curl_max_timeout,
                                                                                                fname,
                                                                                                ipfs_master_api_baseurl,
                                                                                                ipfs_master_api_port,
                                                                                                api))
            logger.info(a1)
            logger.info(b1)
            os.remove(fname)
            self.assertIn("200 OK", a1)

            # Get hash value.
            Hash = json.loads(b1)["Hash"]
            api_cat = b.get_api_v0_file_cat("api")

            for nod in ipfs_slave_l:
                logger.info("---node:%s---" % nod)
                n_url = nod["url"]
                n_eport = nod["eport"]
                logger.info("%s cat:" % nod)
                a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s?arg=%s\"" % (
                                                                                        curl_connect_timeout,
                                                                                        curl_max_timeout,
                                                                                        n_url,
                                                                                        n_eport,
                                                                                        api_cat, Hash))
                logger.info(a1)
                logger.info(b1)

                self.assertIn("200 OK", a1)

                # Create random file name.
                fname = "%s_%s" % (str(i), self.f.random_str())
                logger.info(fname)
                current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                with open(fname, "w") as f:
                    f.write("[%s] [%s] [%s].\n This file should be cat by other nodes." % (
                        current, os.path.basename(__file__), sys._getframe().f_code.co_name))
                f.close()

                # Add the file.
                logger.info("%s add:" % nod)
                a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v -F file=@%s \"%s:%s%s?pin=1\"" % (
                                                                                    curl_connect_timeout,
                                                                                    curl_max_timeout,
                                                                                    fname,
                                                                                    ipfs_master_api_baseurl,
                                                                                    ipfs_master_api_port,
                                                                                    api))
                logger.info(a1)
                logger.info(b1)
                os.remove(fname)
                self.assertIn("200 OK", a1)
                Hash = json.loads(b1)["Hash"]
