# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/15'
"""

import unittest, sys
sys.path.append("../")
import read_conf
from function.func import *
from function.ela_log import MyLog


log = MyLog.get_log()
logger = log.get_logger()

b = read_conf.ReadData()

normal_response_code = b.get_common("normal_response_code")
abnormal_response_code = b.get_common("abnormal_response_code")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")
quiet_param_r = b.get_common("quiet_param_r")
quiet_param_e = b.get_common("quiet_param_e")

api = b.get_pins_recover("api")

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")
curl_connect_timeout = a.get_ipfs_cluster("curl_connect_timeout")
curl_max_timeout = a.get_ipfs_cluster("curl_max_timeout")

api_temp = b.get_pins_recover("api_temp")
api_err = b.get_pins_recover("api_err")


class PinsRecover(unittest.TestCase):
    '''
    Attempt to re-pin/unpin CIDs in error state

    METHOD:	POST Arguments
    Arguments	Type	Required	Description
    arg	string	no	the object CID that need sync.
    local	bool	no	sync HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200.

    [
        {
            "Cid": "<string>",
            "peer_map":
            {
                "Peer ID String"
                {
                    "cid": "<string>",
                    "peer": "<string>",
                    "peername": "<string>",
                    "status": "<string>",
                    "timestamp": "<string>",
                    "error": "<string>"
                }
            }
        }
    ]

    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        self.c = CaseMethod(api, "{}")
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case(os.path.basename(__file__))
    def test_no_argument_post(self):
        code, bcheck = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        self.assertEqual(bcheck, abnormal_response_code)

    @ConfigHttp.wrap_case(os.path.basename(__file__))
    def test_with_correct_argument_post(self):
        a1, b1 = self.f.run_cmd("curl -X POST --connect-timeout %s -m %s -v \"%s:%s%s\"" % (
            curl_connect_timeout,
            curl_max_timeout,
            ipfs_master_api_baseurl,
            ipfs_master_api_port,
            api_temp))
        logger.info(a1)
        logger.info(b1)
        self.assertIn("200 OK", a1)

    @ConfigHttp.wrap_case(os.path.basename(__file__))
    def test_with_incorrect_argument_post(self):
        cc = CaseMethod(api_err, "{}")
        code, bcheck = cc.post_check()
        self.assertEqual(code, abnormal_response_code)
