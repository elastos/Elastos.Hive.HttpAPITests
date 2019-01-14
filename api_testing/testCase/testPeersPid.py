# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/14'
"""

import unittest,sys,json
sys.path.append("../")
import read_conf
from function.func import *
from function.ela_log import MyLog

log = MyLog.get_log()
logger = log.get_logger()

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

b = read_conf.ReadData()
abnormal_response_code = b.get_common("abnormal_response_code")
normal_response_code = b.get_common("normal_response_code")
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")

api = b.get_peers_pid("api")


class PeersPid(unittest.TestCase):
    '''
    Remove a cluster peer from the cluster.

    METHOD:	DELETE Arguments
    Arguments	Type	Required	Description
    peerID	string	yes	a string format of peer id.
    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case
    def test_no_peerid_delete(self):
        code, bcheck = self.f.curl_cmd("curl -X DELETE %s:%s%s" % (ipfs_master_api_baseurl, ipfs_master_api_port, api))
        self.assertEqual(bcheck.strip(), "404 page not found")

    @ConfigHttp.wrap_case
    def test_error_peerid_delete(self):
        code, bcheck = self.f.curl_cmd("curl -X DELETE %s:%s%s/XXX" % (ipfs_master_api_baseurl, ipfs_master_api_port, api))
        d = json.loads(bcheck)
        self.assertEqual(d["code"], 400)


# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(PeersPid("test_error_peerid_delete"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)