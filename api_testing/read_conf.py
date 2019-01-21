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

    def get_common(self, name):
        value = self.data_content.get("common", name)
        return value

    def get_peers(self, name):
        value = self.data_content.get("PEERS", name)
        return value

    def get_peers_pid(self, name):
        value = self.data_content.get("PEERS_PID", name)
        return value

    def get_pins(self, name):
        value = self.data_content.get("PINS", name)
        return value

    def get_pins_cid_sync(self, name):
        value = self.data_content.get("PINS_CID_SYNC", name)
        return value

    def get_pins_recover(self, name):
        value = self.data_content.get("PINS_RECOVER", name)
        return value

    def get_api_v0_uid_new(self, name):
        value = self.data_content.get("API_V0_UID_NEW", name)
        return value

    def get_api_v0_uid_login(self, name):
        value = self.data_content.get("API_V0_UID_LOGIN", name)
        return value

    def get_api_v0_pin_add(self, name):
        value = self.data_content.get("API_V0_PIN_ADD", name)
        return value

    def get_api_v0_pin_ls(self, name):
        value = self.data_content.get("API_V0_PIN_LS", name)
        return value

    def get_api_v0_pin_rm(self, name):
        value = self.data_content.get("API_V0_PIN_RM", name)
        return value