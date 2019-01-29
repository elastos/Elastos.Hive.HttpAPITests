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
api = b.get_api_v0_name_publish("api")
normal_response_body = b.get_api_v0_name_publish("normal_response_body")


class ApiV0NamePublish(unittest.TestCase):
    '''
    Publish user context file or directory to public.

    METHOD:	GET/POST Arguments
    Arguments	Type	Required	Description
    uid	string	yes	a uid for to identify a filesystem context.
    lifetime	string	no	Time duration that the record will be valid for. This accepts durations such as “300s”, “1.5h” or “2h45m”. Valid time units are “ns”, “us” (or “µs”), “ms”, “s”, “m”, “h”. Default: “24h”. Required: no.
    path	string	yes	the file object(IPFS path) to be published. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
        "Name": "<string>"
        "Value": "<string>"
    }
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        self.c = CaseMethod(api, normal_response_body, "ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_no_arg_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_err_arg_get(self):
        temp_api = api + "?arg=xxxx"
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "500")

    @Wrappers.wrap_case(os.path.basename(__file__))
    def test_with_correct_arg_get(self):
        # Create new uid
        uid = self.f.get_new_id(ipfs_master_api_baseurl, ipfs_master_api_port)
        logger.info(uid)

        # Create new path
        path_name = "/%s" % self.f.random_str()
        res, code = self.f.get_files_mkdir(ipfs_master_api_baseurl, ipfs_master_api_port, uid, path_name)
        self.assertEqual(code, "200")

        # Get path hash string
        path_hash = self.f.get_files_path_hash(ipfs_master_api_baseurl, ipfs_master_api_port, path_name, uid)

        # Publish
        temp_api = "%s/uid=%s&path=%s" % (api, uid, path_hash)
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "200")
