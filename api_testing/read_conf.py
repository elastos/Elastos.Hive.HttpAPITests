# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'suxx'
__mtime__ = '2018/12/29'
"""
import os
import ConfigParser

pro_dir = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(pro_dir, "config")
ipfs_config_path = os.path.join(config_path, "ipfs.conf")

data_path = os.path.join(pro_dir, "testFiles")
ipfs_data_path = os.path.join(data_path, "data.conf")

class ReadConfig:
    def __init__(self):
        self.conf_content = ConfigParser.ConfigParser()
        self.conf_content.read(ipfs_config_path)

    def get_ipfs_cluster(self, name):
        value = self.conf_content.get("IPFS_CLUSTER", name)
        return value


class ReadData:
    def __init__(self):
        self.data_content = ConfigParser.ConfigParser()
        self.data_content.read(ipfs_data_path)

    def get_version(self, name):
        value = self.data_content.get("VERSION", name)
        return value

    def get_keylist(self, name):
        value = self.data_content.get("KEYLIST", name)
        return value

    def get_id(self, name):
        value = self.data_content.get("ID", name)
        return value