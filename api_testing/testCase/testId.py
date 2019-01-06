# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2019/1/4'
"""
import read_conf
import unittest,sys,json,os
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
normal_response_code = b.get_id("normal_response_code")
normal_response_body = b.get_id("normal_response_body")


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
