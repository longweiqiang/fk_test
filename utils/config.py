#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 17:35
# @Author  : Weiqiang.long
# @Site    : 
# @File    : config.py
# @Software: PyCharm

"""
读取配置。这里配置文件用的yaml，也可用其他如XML,INI等，需在file_reader中添加相应的Reader进行处理。
"""
import json
import os
from utils.file_reader import YamlReader,IniReader
from utils.extractor import JMESPathExtractor
import configparser

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
# 之前直接拼接的路径，修改了一下，用现在下面这种方法，可以支持linux和windows等不同的平台，也建议大家多用os.path.split()和os.path.join()，不要直接+'\\xxx\\ss'这样
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

INICONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.ini')

DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
TEST_PATH = os.path.join(BASE_PATH, 'testCase')
IMG_PATH = os.path.join(BASE_PATH, 'img')



class Config:
    """
    :param config默认选择CONFIG_FILE，如需访问其他yml文件，可单独传入config
    :调用方法:URL1 = Config(config=CONFIG_FILE1).get('URL')
    """
    def __init__(self, path='public', config='url_config.yml'):
        CONFIG_FILE = os.path.join(BASE_PATH, 'data', path, config)

        self.config = YamlReader(CONFIG_FILE).data

    def get(self, element, index=0):
        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        """
        return self.config[index].get(element)




class IniConfig:
    def __init__(self, inif=INICONFIG_FILE):
        self.iniconfig = IniReader.iniConfig
        self.config = configparser.ConfigParser()
        self.config.read(inif)

    def get(self, name, element=None):
        config = self.config.get(name, element)
        return config

    # def set(self, name, element):



class JsonConfig():
    """
    获取json配置文件方法
    """
    def __init__(self, path='public', jsonpath='public_jxyp_config.json'):
        """
        :param jsonpath: 配置文件的路径
        """
        JSONCONFIG_FILE = os.path.join(BASE_PATH, 'data', path, jsonpath)
        self._j = JMESPathExtractor()
        self._jsonConfig = YamlReader(JSONCONFIG_FILE).data
        self._content = open(JSONCONFIG_FILE, encoding='utf-8')

    def get_jsondata(self, element=None):
        """
        :param element: 需要获取json的对应key;如data.item.loginStatus;此字段为空时,默认返回字符串中所有内容
        :return: 返回对应的字符串数据
        """
        if element==None:
            self.rights = json.load(self._content)
        else:
            self._all_rights = json.load(self._content)
            # 把self._all_rights的值转成字符串,这样下面的self._j.extract方法才能识别
            self.contents = json.dumps(self._all_rights)
            self.rights = self._j.extract(query=element, body=self.contents)
        return self.rights

# a = IniConfig().get('DB', 'host')
# print(a)