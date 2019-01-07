# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/4'
"""
import read_conf
import unittest,sys,json
sys.path.append("../")
from function.func import *
from function.ela_log import MyLog


log = MyLog.get_log()
logger = log.get_logger()

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

b = read_conf.ReadData()
api = b.get_id("api")
normal_response_code = b.get_common("normal_response_code")
not_found_code = b.get_common("not_found_code")

normal_response_body = b.get_id("normal_response_body")
verbose_param_r = b.get_id("verbose_param_r")
verbose_param_e = b.get_id("verbose_param_e")


class Id(unittest.TestCase):
    '''
    Show the cluster peers and its daemon information

    Arguments

    Arguments	Type	Required	Description
    verbose	bool	no	display all extra information.
    HTTP Response

    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
          "id": "<NodeId>",
          "peers": [
                  "/ip4/104.236.176.52/tcp/4001",
                  "/ip4/104.236.176.52/tcp/4001"
          ]
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case
    def test_normal_get(self):
        # Check code 200
        o, e = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(o)
        logger.info(e)
        self.assertEqual(e, normal_response_code)
        # Check body
        o, e = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(o)
        logger.info(e)
        res_dict = json.loads(e)
        expect_dict = json.loads(normal_response_body)
        res = self.f.check_body(res_dict, expect_dict)
        self.assertEqual(res, 0)

    @ConfigHttp.wrap_case
    def test_normal_post_404(self):
        # Check code 404
        o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(o)
        logger.info(e)
        self.assertEqual(e, not_found_code)

    @ConfigHttp.wrap_case
    def test_with_verbose_get(self):
        verbose_cases_r = verbose_param_r.split(",")
        for verbose in verbose_cases_r:
            api_str = "%s?%s" % (api, verbose)
            # Check code 200
            o, e = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_str)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, normal_response_code)
            # Check body
            o, e = self.f.curl_get_body(ipfs_master_api_baseurl, ipfs_master_api_port, api_str)
            logger.info(o)
            logger.info(e)
            res_dict = json.loads(e)
            expect_dict = json.loads(normal_response_body)
            res = self.f.check_body(res_dict, expect_dict)
            self.assertEqual(res, 0)

        verbose_cases_e = verbose_param_e.split(",")
        for verbose in verbose_cases_e:
            api_str = "%s?%s" % (api, verbose)
            o, e = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api_str)
            logger.info(o)
            logger.info(e)
            # self.assertEqual(e, abnormal_response_code)
            self.assertEqual(e, normal_response_code)


# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Id("test_with_verbose_get"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
