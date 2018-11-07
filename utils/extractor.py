#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/28 10:53
# @Author  : Weiqiang.long
# @Site    : 
# @File    : extractor.py
# @Software: PyCharm

"""抽取器，从响应结果中抽取部分数据"""

import json
import jmespath


class JMESPathExtractor(object):
    """
    用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self, query=None, body=None):
        try:
            return jmespath.search(query, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))

    def addextract(self, query=None, body=None):
        json_data = json.dumps(body)
        try:
            return jmespath.search(query, json.loads(json_data))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))