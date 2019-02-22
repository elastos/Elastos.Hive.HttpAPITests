# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/7'
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

normal_response_code = b.get_common("normal_response_code")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")

ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")
curl_connect_timeout = a.get_ipfs_cluster("curl_connect_timeout")
curl_max_timeout = a.get_ipfs_cluster("curl_max_timeout")

api = b.get_peers("api")
normal_response_body = b.get_peers("normal_response_body")
peers_case = b.get_peers("200_code_cases")


class Peers(unittest.TestCase):
    '''
    List the cluster servers with open connections.

    METHOD:	GET Arguments
    Arguments	Type	Required	Description
    verbose	bool	no	display all extra information. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
          "data": [
            "/ip4/104.236.176.52/tcp/4001",
            "/ip4/104.236.176.52/tcp/4001"
          ]
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case(os.path.basename(__file__))
    def test_normal_get(self):
        a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s\"" % (curl_connect_timeout,
                                                                                    curl_max_timeout,
                                                                                    ipfs_master_api_baseurl,
                                                                                    ipfs_master_api_port, api))
        logger.info(b1)
        self.assertIn("200 OK", a1)

    @ConfigHttp.wrap_case(os.path.basename(__file__))
    def test_with_verbose_get(self):
        verbose_cases_r = verbose_param_r.split(",")
        for verbose in verbose_cases_r:
            a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s?%s\"" % (curl_connect_timeout,
                                                                                           curl_max_timeout,
                                                                                           ipfs_master_api_baseurl,
                                                                                           ipfs_master_api_port,
                                                                                           api, verbose))
            logger.info(b1)
            self.assertIn("200 OK", a1)

        verbose_cases_e = verbose_param_e.split(",")
        for verbose in verbose_cases_e:
            a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s?%s\"" % (curl_connect_timeout,
                                                                                           curl_max_timeout,
                                                                                           ipfs_master_api_baseurl,
                                                                                           ipfs_master_api_port,
                                                                                           api, verbose))
            logger.info(b1)
            self.assertIn("200 OK", a1)

    @ConfigHttp.wrap_case(os.path.basename(__file__))
    def test_200_cases_get(self):
        p_c = self.f.list_conf_case(peers_case)
        for p in p_c:
            a1, b1 = self.f.run_cmd("curl --connect-timeout %s -m %s -v \"%s:%s%s?%s\"" % (curl_connect_timeout,
                                                                                        curl_max_timeout,
                                                                                        ipfs_master_api_baseurl,
                                                                                        ipfs_master_api_port,
                                                                                        api, p))
            logger.info(b1)
            self.assertIn("200 OK", a1)

