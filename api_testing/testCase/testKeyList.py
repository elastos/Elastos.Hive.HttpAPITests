# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/4'
"""
import unittest,sys,json,os
sys.path.append("../")
from function.func import *
from function.ela_log import MyLog

import read_conf
log = MyLog.get_log()
logger = log.get_logger()
a = read_conf.ReadConfig()
b = read_conf.ReadData()

ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

api = b.get_keylist("api")

class KeyList(unittest.TestCase):
    '''
    List all keypairs in the given peer

    Arguments

    Arguments	Type	Required	Description
    name	string	yes	name of key to create.
    type	string	no	type of the key to create [rsa, ed25519].
    size	int	no	size of the key to generate.
    HTTP Response

    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
        "data": {
            "Name": "<string>",
            "Id": "<string>"
        },
        "desciption": "<string>"
    }
    '''





# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Version("test_with_repo_post"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
