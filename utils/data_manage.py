#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/27 9:53
# @Author  : Weiqiang.long
# @Site    : 
# @File    : data_manage.py
# @Software: PyCharm

import oss2
from urllib import parse
import re

class is_None():
    """判断一个数据是否是tuple类型的None"""
    def __init__(self, t_data, items=0):
        """
        :param t_data: tuple类型的一个数据,接收后转换成str类型的,并读取tuple数据中下标为0的数据
        :param items: 需要取的数据对应的下标
        """
        try:
            self.data = str(t_data[items])
        except TypeError:
            print('数据不存在')


    def is_none(self):
        """
        :return: 转换后的数据,用一个变量接收即可
        """
        if self.data == 'None':
            self.data = ''
        else:
            self.data = self.data
        return self.data

    def in_dict(key, value):
        '''
        :param key: dict路径
        :param value: 实际校验值
        :return:
        '''
        # a = ''
        # try:
        #     a = dict_dir
        #     print(a)
        # except KeyError as e:
        #     print(e,'不存在')

        if key == value:
            return 'success'
        else:
            return 'key存在,但断言失败'

class Get_oss:

    def get_oss(path, time=4):
        """
        生成签名URL
        :param path:文件名
        :param time:授权有效期,默认授权有效期为四天
        :return:签名URL
        """
        # MyAccessKeyId = 'LTAIyxkt6Uz6Lmob'
        # MyAccessKeySecret = 'GMr5YsbuwPyiluxnclDTbfBRyWXYGl'
        # MyEndpoint = 'oss-cn-hangzhou.aliyuncs.com'
        # MyBucketName = 'lwq573925242'

        MyAccessKeyId = 'LTAIGtLs9U0rENY6'
        MyAccessKeySecret = 'aXsG49CtClh3LRDlLMbdzReDx1gmrq'
        MyEndpoint = 'oss-cn-hangzhou.aliyuncs.com'
        MyBucketName = 'xjx-files'

        # 换算time,用天数乘以86400秒(一天)
        times = time * 86400
        # print(times)

        auth = oss2.Auth(MyAccessKeyId, MyAccessKeySecret)
        bucket = oss2.Bucket(auth, MyEndpoint, MyBucketName)
        oss_url = bucket.sign_url('GET', path, times)
        return oss_url

    def get_url(url):
        # 解码url
        # url_org = urllib.unquote(self.url)
        url_org = parse.unquote(url)
        return url_org

class Str_info:

    def str_info(self, data ,items=24):
        """
        :param items: 截取的开始下标
        :param data: 需要截取的数据
        :return: 截取完成并取消数据中/的数据
        """
        d = data[items:]
        strinfo = re.compile('/')
        data_info = strinfo.sub('', d)
        return data_info





# # 调用get_oss方法
# a = Get_oss.get_oss('files/newfiles/20181025/20181025160102_4hru7wby6p_appTh.png')
# print(a)
# # 调用get_url方法
# b = Get_oss.get_url('http://xjx-files.oss-cn-hangzhou.aliyuncs.com/files%2Fnewfiles%2F20181025%2F20181025160102_4hru7wby6p_appTh.png?OSSAccessKeyId=LTAIGtLs9U0rENY6&Expires=1541300854&Signature=TAfuqb5rvzmG1Gt4ceJUa8JXygo%3D')
# print(b)

