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
not_found_code = b.get_common("not_found_code")
verbose_param_r = b.get_common("verbose_param_r")
verbose_param_e = b.get_common("verbose_param_e")
quiet_param_r = b.get_common("quiet_param_r")
quiet_param_e = b.get_common("quiet_param_e")

api = b.get_pins_cid_sync("api")

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")
# pins_case = b.get_pins_cid_sync("200_code_cases")


class PinsRecover:
    '''
    Attempt to re-pin/unpin CIDs in error state

    METHOD:	POST Arguments
    Arguments	Type	Required	Description
    arg	string	no	the object CID that need sync.
    local	bool	no	sync HTTP Response
    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    '''

