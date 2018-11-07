#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/8 17:26
# @Author  : Weiqiang.long
# @Site    : 
# @File    : test_ini.py
# @Software: PyCharm

import os
import configparser

# BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# INICONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.ini')
#
# config=configparser.ConfigParser()
# config.read(INICONFIG_FILE)


# import sys
# import os
# p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
# print(p)
# a = os.path.join(p, 'utils')
# print(a)
#
# sys.path.append(a)
from utils.config import IniConfig

DBHOST = IniConfig().get('DB', 'host')
print(DBHOST)

# c = config.get('DB', 'host')
# print(c)