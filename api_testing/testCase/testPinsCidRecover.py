# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/15'
"""

# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/15'
"""

import unittest, sys, copy

sys.path.append("../")
import read_conf
from function.func import *
from function.ela_log import MyLog

log = MyLog.get_log()
logger = log.get_logger()

b = read_conf.ReadData()

normal_response_code = b.get_common("normal_response_code")
api = b.get_pins_cid_sync("api")

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")
ipfs_master_api_endpoint_port = a.get_ipfs_cluster("ipfs_master_api_endpoint_port")

normal_response_body = b.get_pins_cid_recover("normal_response_body")


class PinsCidRecover(unittest.TestCase):
    '''
    Recover a CID

    METHOD:	POST
    Arguments	Type	Required	Description
    cid	string	no	the object CID that need sync. HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp("ipfs_master_api_endpoint_port")
        unittest.TestCase.__init__(self, methodName)

    @Wrappers.wrap_case
    def test_without_cid_post(self):
        temp_api = "%s/recover" % api
        a1, b1 = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(b1)
        self.assertEqual(b1, "400")

    @Wrappers.wrap_case
    def test_with_correct_cid_post(self):
        fname = self.f.random_str()
        logger.info(fname)
        with open(fname, "a") as f:
            f.write("This is file %s\n" % fname)
        f.close()

        # Add the file.
        a1, b1 = self.f.run_cmd("curl -F file=@%s %s:%s/api/v0/file/add" % (fname, ipfs_master_api_baseurl,
                                                                            ipfs_master_api_endpoint_port))
        logger.info(b1)
        cid = json.loads(b1)["Hash"]
        os.remove(fname)

        temp_api = "%s/%s/recover" % (api, cid)
        a1, b1 = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(a1)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @Wrappers.wrap_case
    def test_with_error_cid_post(self):
        cid = "Qm%s" % self.f.random_str(44)

        temp_api = "%s/%s/recover" % (api, cid)
        a1, b1 = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
        logger.info(a1)
        logger.info(b1)
        self.assertEqual(b1, "400")
