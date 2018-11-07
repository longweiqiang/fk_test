#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 15:16
# @Author  : Weiqiang.long
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import os
import ast
import requests
from requests.auth import HTTPBasicAuth
import time
import unittest
from utils.dbconfig import dbHandle
from utils import data_manage
from utils.config import IniConfig

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
test_data_file = os.path.join(BASE_PATH, 'config', 'test_data.ini')

class jsxjx_self_data(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        get_test_data = IniConfig(inif=test_data_file)
        # 获取接口地址
        api_host = get_test_data.get('JSBX', 'api_host')

        # 获取接口数据
        test_data = get_test_data.get('JSBX', 'test_data')
        # 使用 ast.literal_eval把test_data从str类型转换成dict类型
        data = ast.literal_eval(test_data)

        # 获取鉴权账号
        basicAuth_name = get_test_data.get('JSBX', 'basicAuth_name')

        # 获取鉴权密码
        basicAuth_password = get_test_data.get('JSBX', 'basicAuth_password')


        self.res = requests.post(url=api_host, json=data, auth=HTTPBasicAuth(basicAuth_name, basicAuth_password))
        print(self.res.text)
        self.dict = self.res.json()

        # 赋值全局变量order.id
        self.order_id = self.dict['body']['order'][0]['id']

        # 赋值全局变量current_order.id
        self.current_order_id = self.dict['body']['current_order']['id']

        # 赋值全局变量user_id
        self.user_id = int(get_test_data.get('JSBX', 'user_id'))

        # 定义商户号--借钱呗
        self.merchant_number = int(get_test_data.get('JSBX', 'merchant_number'))

        # 声明全局变量first_mobile
        global first_mobile

        self.is_none = data_manage

        self.get_oss = data_manage.Get_oss


    def setUp(self):
        '''只能用setUp,因为每次调用db后，有close方法会断开db连接，需要每个case执行前重新连接'''
        self.db = dbHandle('DB')

        # 定义大数据数据库
        # self.big_db = dbHandle('BIGDB')

    def test_01_http_code(self):
        '''判断http状态码'''
        # print(self.res.status_code)
        self.assertEqual(self.res.status_code, 200)

    def test_02_diy_code(self):
        '''判断自定义code'''
        data = self.dict['code']
        self.assertEqual(data, 200)

    def test_03_message(self):
        '''判断message'''
        data = self.dict['message']
        self.assertEqual(data, 'success')

    def test_04_body_order_01_id(self):
        '''判断body.order[0]id'''
        data = self.dict['body']['order'][0]['id']
        sql = 'SELECT id FROM asset_borrow_order where id = {0} '.format(self.order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_05_body_order_01_order_type(self):
        '''判断body.order[0]order_type'''
        data = self.dict['body']['order'][0]['order_type']
        sql = 'SELECT order_type FROM asset_borrow_order where id = {0} '.format(self.order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_06_body_order_01_money_amount(self):
        '''判断body.order[0]money_amount'''
        data = self.dict['body']['order'][0]['money_amount']
        sql = 'SELECT money_amount FROM asset_borrow_order where id = {0} '.format(self.order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_07_body_order_01_apr(self):
        '''判断body.order[0]apr'''
        data = self.dict['body']['order'][0]['apr']
        sql = 'SELECT apr/loan_term*365/10 FROM asset_borrow_order where id = {0} '.format(self.order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        # 返回的年化借款利率是浮点型，需要去除小数部分，所以用str(int())嵌套
        data2 = str(int(data1[0]))
        self.assertEqual(data, data2)

    def test_08_body_order_01_loan_method(self):
        '''判断body.order[0]loan_method'''
        data = self.dict['body']['order'][0]['loan_method']
        sql = 'SELECT loan_method FROM asset_borrow_order where id = {0} '.format(self.order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_09_body_order_01_loan_term(self):
        '''判断body.order[0]loan_term'''
        data = self.dict['body']['order'][0]['loan_term']
        sql = 'SELECT loan_term FROM asset_borrow_order where id = {0} '.format(self.order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_10_body_order_01_time(self):
        '''判断body.order[0]time'''
        data = self.dict['body']['order'][0]['time']
        sql = 'SELECT order_time FROM asset_borrow_order where id = {0} '.format(self.order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换成时间戳的形式进行断言对比
        timeArray = time.strptime(data2, "%Y-%m-%d %H:%M:%S")
        order_time = str(int(time.mktime(timeArray)))
        # print(order_time)
        self.assertEqual(data, order_time)

    def test_11_body_order_01_client_type(self):
        '''判断body.order[0]client_type'''
        data = self.dict['body']['order'][0]['client_type']
        sql = 'SELECT client_type FROM asset_borrow_order where id = {0} '.format(self.order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换一下，把android转换成'1',ios转成'2',其他类型转成'3'
        if data2 == 'android':
            data2 = '1'
        elif data2 == 'ios':
            data2 = '2'
        else:
            data2 = '3'

        self.assertEqual(data, data2)

    def test_12_body_order_01_status(self):
        '''判断body.order[0]status'''
        data = self.dict['body']['order'][0]['status']
        sql = 'SELECT status FROM asset_borrow_order where id = {0} '.format(self.order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # status字段现金侠和风控的状态有些不一致，需要转换一下
        if data2 == '0':    # 待初审(待机审)
            data2 = '0'
        elif data2 == '-3': # 初审驳回
            data2 = '-3'
        elif data2 == '1':  # 初审通过
            data2 = '7'
        elif data2 == '-4': # 复审驳回
            data2 = '-4'
        elif data2 == '20': # 复审通过,待放款
            data2 = '2'
        elif data2 == '-5': # 放款驳回
            data2 = '-9'
        elif data2 == '22': # 放款中
            data2 = '2'
        elif data2 == '-10':    # 放款失败
            data2 = '-9'
        elif data2 == '21': # 已放款，还款中
            data2 = '3'
        elif data2 == '23': # 部分还款
            data2 = '3'
        elif data2 == '30': # 已还款
            data2 = '6'
        elif data2 == '-11':    # 已逾期
            data2 = '3'
        elif data2 == '-20':    # 已坏账
            data2 = '3'
        elif data2 == '34': # 逾期已还款
            data2 = '6'
        self.assertEqual(data, data2)

    def test_13_body_order_01_is_depository(self):
        '''判断body.order[0]is_depository'''
        data = self.dict['body']['order'][0]['is_depository']
        sql = 'SELECT event_type FROM user_card_info WHERE user_id = {0} '.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 需要判断user_card_info表中的event_type字段，0为非存管，1为存管
        if data2 == '0':
            data2 = '0'
        elif data2 == '1':
            data2 = '1'
        self.assertEqual(data, data2)

    def test_14_body_order_01_len(self):
        '''判断body.order总订单数量'''
        data = str(len(self.dict['body']['order']))
        sql = 'SELECT count(*) FROM asset_borrow_order where user_id = {0} '.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_15_body_repayment_period_01_id(self):
        '''判断body.repayment_period[0]id'''
        data = self.dict['body']['repayment_period'][0]['id']
        sql = 'SELECT id FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_16_body_repayment_period_01_order_id(self):
        '''判断body.repayment_period[0]order_id'''
        data = self.dict['body']['repayment_period'][0]['order_id']
        sql = 'SELECT asset_order_id FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_17_body_repayment_period_01_plan_repayment_money(self):
        '''判断body.repayment_period[0]plan_repayment_money'''
        data = self.dict['body']['repayment_period'][0]['plan_repayment_money']
        sql = 'SELECT repayment_amount FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_18_body_repayment_period_01_user_id(self):
        '''判断body.repayment_period[0]user_id'''
        data = self.dict['body']['repayment_period'][0]['user_id']
        sql = 'SELECT user_id FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_19_body_repayment_period_01_period(self):
        '''判断body.repayment_period[0]period'''
        data = self.dict['body']['repayment_period'][0]['period']
        # 小额只有1期但订单，此处暂时不考虑大额
        data1 = '1'
        self.assertEqual(data, data1)

    def test_20_body_repayment_period_01_plan_repayment_time(self):
        '''判断body.repayment_period[0]plan_repayment_time'''
        data = self.dict['body']['repayment_period'][0]['plan_repayment_time']
        sql = 'SELECT repayment_time FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换成时间戳的形式进行断言对比
        timeArray = time.strptime(data2, "%Y-%m-%d %H:%M:%S")
        plan_repayment_time = str(int(time.mktime(timeArray)))
        self.assertEqual(data, plan_repayment_time)

    def test_21_body_repayment_period_01_counter_fee(self):
        '''判断body.repayment_period[0]counter_fee'''
        data = self.dict['body']['repayment_period'][0]['counter_fee']
        # 项目没有服务费的定义，所以统一都是0
        data1 = '0'
        self.assertEqual(data, data1)

    def test_22_body_repayment_period_01_true_repayment_money(self):
        '''判断body.repayment_period[0]true_repayment_money'''
        data = self.dict['body']['repayment_period'][0]['true_repayment_money']
        sql = 'SELECT repaymented_amount FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_23_body_repayment_period_01_true_repayment_time(self):
        '''判断body.repayment_period[0]true_repayment_time'''
        data = self.dict['body']['repayment_period'][0]['true_repayment_time']
        sql = 'SELECT repayment_real_time FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换成时间戳的形式进行断言对比
        timeArray = time.strptime(data2, "%Y-%m-%d %H:%M:%S")
        repayment_real_time = str(int(time.mktime(timeArray)))
        self.assertEqual(data, repayment_real_time)

    def test_24_body_repayment_period_01_interests(self):
        '''判断body.repayment_period[0]interests'''
        data = self.dict['body']['repayment_period'][0]['interests']
        sql = 'SELECT repayment_interest FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_25_body_repayment_period_01_late_fee(self):
        '''判断body.repayment_period[0]late_fee'''
        data = self.dict['body']['repayment_period'][0]['late_fee']
        sql = 'SELECT plan_late_fee FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_26_body_repayment_period_01_principal(self):
        '''判断body.repayment_period[0]principal'''
        data = self.dict['body']['repayment_period'][0]['principal']
        sql = 'SELECT repayment_principal FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_27_body_repayment_period_01_late_day(self):
        '''判断body.repayment_period[0]late_day'''
        data = self.dict['body']['repayment_period'][0]['late_day']
        sql = 'SELECT late_day FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    @unittest.skip('先跳过')
    def test_28_body_repayment_period_01_is_overdue(self):
        # TODO 需要找开发确认repayment_period.is_overdue字段是怎么判断的
        '''判断body.repayment_period[0]is_overdue'''
        data = self.dict['body']['repayment_period'][0]['is_overdue']
        sql = 'SELECT late_day FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    @unittest.skip('先跳过')
    def test_29_body_repayment_period_01_coupon_money(self):
        # TODO 需要找开发确认repayment_period.coupon_money字段是怎么判断的
        '''判断body.repayment_period[0]coupon_money'''
        data = self.dict['body']['repayment_period'][0]['coupon_money']
        sql = 'SELECT late_day FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    @unittest.skip('先跳过')
    def test_30_body_repayment_period_01_status(self):
        # TODO 需要找开发确认repayment_period.status字段是怎么判断的
        '''判断body.repayment_period[0]status'''
        data = self.dict['body']['repayment_period'][0]['status']
        sql = 'SELECT late_day FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    @unittest.skip('先跳过')
    def test_31_body_repayment_period_01_next_loan_advice(self):
        # TODO 需要找开发确认repayment_period.next_loan_advice字段是怎么判断的
        '''判断body.repayment_period[0]next_loan_advice'''
        data = self.dict['body']['repayment_period'][0]['next_loan_advice']
        sql = 'SELECT late_day FROM asset_repayment WHERE user_id = {0} LIMIT 1'.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_32_body_repayment_period_01_len(self):
        '''判断body.repayment_period总订单数量'''
        data = str(len(self.dict['body']['repayment_period']))
        sql = 'SELECT count(*) FROM asset_repayment where user_id = {0} '.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_33_body_current_order_01_id(self):
        '''判断body.current_order.id'''
        data = self.dict['body']['current_order']['id']
        sql = 'SELECT id FROM asset_borrow_order WHERE id = {0}'.format(self.current_order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_34_body_current_order_01_order_type(self):
        '''判断body.current_order.order_type'''
        data = self.dict['body']['current_order']['order_type']
        sql = 'SELECT order_type FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_35_body_current_order_01_money_amount(self):
        '''判断body.current_order.money_amount'''
        data = self.dict['body']['current_order']['money_amount']
        sql = 'SELECT money_amount FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_36_body_current_order_01_apr(self):
        '''判断body.current_order.apr'''
        data = self.dict['body']['current_order']['apr']
        sql = 'SELECT apr/loan_term*365/10 FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        # 返回的年化借款利率是浮点型，需要去除小数部分，所以用str(int())嵌套
        data2 = str(int(data1[0]))
        self.assertEqual(data, data2)

    def test_37_body_current_order_loan_method(self):
        '''判断body.current_order.loan_method'''
        data = self.dict['body']['current_order']['loan_method']
        sql = 'SELECT loan_method FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_38_body_current_order_loan_term(self):
        '''判断body.current_order.loan_term'''
        data = self.dict['body']['current_order']['loan_term']
        sql = 'SELECT loan_term FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_39_body_current_order_time(self):
        '''判断body.current_order.time'''
        data = self.dict['body']['current_order']['time']
        sql = 'SELECT order_time FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换成时间戳的形式进行断言对比
        timeArray = time.strptime(data2, "%Y-%m-%d %H:%M:%S")
        order_time = str(int(time.mktime(timeArray)))
        # print(order_time)
        self.assertEqual(data, order_time)

    def test_40_body_current_order_client_type(self):
        '''判断body.current_order.client_type'''
        data = self.dict['body']['current_order']['client_type']
        sql = 'SELECT client_type FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换一下，把android转换成'1',ios转成'2',其他类型转成'3'
        if data2 == 'android':
            data2 = '1'
        elif data2 == 'ios':
            data2 = '2'
        else:
            data2 = '3'
        self.assertEqual(data, data2)

    def test_41_body_current_order_status(self):
        '''判断body.current_order.status'''
        data = self.dict['body']['current_order']['status']
        sql = 'SELECT status FROM asset_borrow_order where id = {0} '.format(self.current_order_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # status字段现金侠和风控的状态有些不一致，需要转换一下
        if data2 == '0':  # 待初审(待机审)
            data2 = '0'
        elif data2 == '-3':  # 初审驳回
            data2 = '-3'
        elif data2 == '1':  # 初审通过
            data2 = '7'
        elif data2 == '-4':  # 复审驳回
            data2 = '-4'
        elif data2 == '20':  # 复审通过,待放款
            data2 = '2'
        elif data2 == '-5':  # 放款驳回
            data2 = '-9'
        elif data2 == '22':  # 放款中
            data2 = '2'
        elif data2 == '-10':  # 放款失败
            data2 = '-9'
        elif data2 == '21':  # 已放款，还款中
            data2 = '3'
        elif data2 == '23':  # 部分还款
            data2 = '3'
        elif data2 == '30':  # 已还款
            data2 = '6'
        elif data2 == '-11':  # 已逾期
            data2 = '3'
        elif data2 == '-20':  # 已坏账
            data2 = '3'
        elif data2 == '34':  # 逾期已还款
            data2 = '6'
        self.assertEqual(data, data2)

    def test_42_body_current_order_is_depository(self):
        '''判断body.current_order.is_depository'''
        data = self.dict['body']['current_order']['is_depository']
        sql = 'SELECT event_type FROM user_card_info WHERE user_id = {0} '.format(self.user_id)
        # print(sql)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 需要判断user_card_info表中的event_type字段，0为非存管，1为存管
        if data2 == '0':
            data2 = '0'
        elif data2 == '1':
            data2 = '1'
        self.assertEqual(data, data2)

    def test_43_body_user_info_user_id(self):
        '''判断body.user_info.user_id'''
        data = self.dict['body']['user_info']['user_id']
        sql = 'SELECT id FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_44_body_user_info_name(self):
        '''判断body.user_info.name'''
        data = self.dict['body']['user_info']['name']
        sql = 'SELECT realname FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_45_body_user_info_phone(self):
        '''判断body.user_info.phone'''
        data = self.dict['body']['user_info']['phone']
        sql = 'SELECT user_phone FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_46_body_user_info_id_number(self):
        '''判断body.user_info.id_number'''
        data = self.dict['body']['user_info']['id_number']
        sql = 'SELECT id_number FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_47_body_user_info_reg_time(self):
        '''判断body.user_info.reg_time'''
        data = self.dict['body']['user_info']['reg_time']
        sql = 'SELECT create_time FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换成时间戳的形式进行断言对比
        timeArray = time.strptime(data2, "%Y-%m-%d %H:%M:%S")
        reg_time = str(int(time.mktime(timeArray)))
        # print(order_time)
        self.assertEqual(data, reg_time)

    def test_48_body_user_info_reg_ip(self):
        '''判断body.user_info.reg_ip'''
        data = self.dict['body']['user_info']['reg_ip']
        sql = 'SELECT create_ip FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_49_body_user_info_customer_type(self):
        '''判断body.user_info.customer_type'''
        data = self.dict['body']['user_info']['customer_type']
        sql = 'SELECT customer_type FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_50_body_user_info_degrees(self):
        '''判断body.user_info.degrees'''
        data = self.dict['body']['user_info']['degrees']
        sql = 'SELECT education FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_51_body_user_info_company_name(self):
        '''判断body.user_info.company_name'''
        data = self.dict['body']['user_info']['company_name']
        sql = 'SELECT company_name FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_52_body_user_info_company_telephone(self):
        '''判断body.user_info.company_telephone'''
        data = self.dict['body']['user_info']['company_telephone']
        sql = 'SELECT company_phone FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_53_body_user_info_company_address(self):
        '''判断body.user_info.company_address'''
        data = self.dict['body']['user_info']['company_address']
        sql = 'SELECT company_address FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_54_body_user_info_live_address(self):
        '''判断body.user_info.live_address'''
        data = self.dict['body']['user_info']['live_address']
        sql = 'SELECT present_address_distinct, present_address FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        data3 = self.is_none.is_None(data1, 1).is_none()
        data4 = data2 + ',' +data3
        self.assertEqual(data, data4)

    def test_55_body_user_info_live_longitude(self):
        '''判断body.user_info.live_longitude'''
        data = self.dict['body']['user_info']['live_longitude']
        sql = 'SELECT present_longitude FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_56_body_user_info_live_latitude(self):
        '''判断body.user_info.live_latitude'''
        data = self.dict['body']['user_info']['live_latitude']
        sql = 'SELECT present_latitude FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_57_body_user_info_live_time_type(self):
        '''判断body.user_info.live_time_type'''
        data = self.dict['body']['user_info']['live_time_type']
        sql = 'SELECT present_period FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    @unittest.skip("暂时跳过")
    def test_58_body_user_info_marriage(self):
        # TODO 现金侠和风控的状态值转换列表
        '''判断body.user_info.marriage'''
        data = self.dict['body']['user_info']['marriage']
        sql = 'SELECT marital_status FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_59_body_user_info_credit_total(self):
        '''判断body.user_info.credit_total'''
        data = self.dict['body']['user_info']['credit_total']
        sql = 'SELECT amount_max FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    # @unittest.skip("暂时跳过")
    def test_60_body_user_info_id_card_count(self):
        # TODO 推给风控的数据是从哪里取的？库里面找不到
        '''判断body.user_info.id_card_count'''
        data = self.dict['body']['user_info']['id_card_count']
        data1 = str(int(data))
        data2 = '3'
        self.assertEqual(data1, data2)

    def test_61_body_user_info_id_card_z_pic_name(self):
        # TODO pic_name字段是哪里的数据？
        '''判断body.user_info.id_card_z[0]pic_name'''
        data = self.dict['body']['user_info']['id_card_z'][0]['pic_name']
        sql = 'SELECT idcard_img_z FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        data3 = self.is_none.Str_info().str_info(data2)
        self.assertEqual(data, data3)

    @unittest.skip("暂时跳过,未找到解决方法")
    def test_62_body_user_info_id_card_z_url(self):
        # TODO oss中渠道的url和自有数据中的url不一致，可能是编码问题导致，后面再解决
        '''判断body.user_info.id_card_z[0]url'''
        data = self.dict['body']['user_info']['id_card_z'][0]['url']
        print(data)
        sql = 'SELECT idcard_img_z FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # print(data2)
        data3 = self.get_oss.get_oss(data2)
        # print(data3)
        data4 = self.get_oss.get_url(data3)
        print(data4)
        # self.assert_equal.__self__.maxDiff = None
        self.maxDiff = None
        self.assertEqual(data, data4)

    def test_63_body_user_info_id_card_f_pic_name(self):
        # TODO 推给风控的数据是从哪里取的？库里面找不到
        '''判断body.user_info.id_card_f[0]pic_name'''
        data = self.dict['body']['user_info']['id_card_f'][0]['pic_name']
        sql = 'SELECT idcard_img_f FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        data3 = self.is_none.Str_info().str_info(data2)
        self.assertEqual(data, data3)

    @unittest.skip("暂时跳过,未找到解决方法")
    def test_64_body_user_info_id_card_f_url(self):
        # TODO oss中渠道的url和自有数据中的url不一致，可能是编码问题导致，后面再解决
        '''判断body.user_info.id_card_f[0]url'''
        data = self.dict['body']['user_info']['id_card_f'][0]['url']
        print(data)
        sql = 'SELECT idcard_img_f FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # print(data2)
        data3 = self.get_oss.get_oss(data2)
        # print(data3)
        data4 = self.get_oss.get_url(data3)
        print(data4)
        # self.assert_equal.__self__.maxDiff = None
        self.maxDiff = None
        self.assertEqual(data, data4)

    def test_65_body_user_info_face_recognition_pic_name(self):
        '''判断body.user_info.face_recognition[0]pic_name'''
        data = self.dict['body']['user_info']['face_recognition'][0]['pic_name']
        sql = 'SELECT head_portrait FROM user_info where id = {0} '.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        data3 = self.is_none.Str_info().str_info(data2)
        self.assertEqual(data, data3)

    def test_66_body_user_info_work_card(self):
        '''判断body.user_info.work_card'''
        data = self.dict['body']['user_info']['work_card']
        data1 = []
        self.assertEqual(data, data1)

    def test_67_body_user_info_is_vip(self):
        # TODO is_vip字段在数据库中未找到，需要和开发确认
        '''判断body.user_info.is_vip'''
        data = self.dict['body']['user_info']['is_vip']
        data1 = str(int(data))
        data2 = '0'
        self.assertEqual(data1, data2)

    def test_68_body_user_info_bank_card(self):
        '''判断body.user_info.bank_card'''
        data = self.dict['body']['user_info']['bank_card']
        # 接口未传值,直接传空字符串
        data1 = ''
        self.assertEqual(data, data1)

    def test_69_body_user_info_credit_card(self):
        '''判断body.user_info.credit_card'''
        data = self.dict['body']['user_info']['credit_card']
        # 接口未传值,直接传空字符串
        data1 = ''
        self.assertEqual(data, data1)

    def test_70_body_user_info_reg_client_type(self):
        '''判断body.user_info.reg_client_type'''
        data = self.dict['body']['user_info']['reg_client_type']
        # 接口未传值,直接传空字符串
        data1 = ''
        self.assertEqual(data, data1)

    def test_71_body_user_info_reg_source(self):
        '''判断body.user_info.reg_source'''
        data = self.dict['body']['user_info']['reg_source']
        sql = 'SELECT channel_name FROM channel_info WHERE id IN (SELECT user_from FROM user_info WHERE id = {0})'.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_72_body_user_contact_first_relation(self):
        '''判断body.user_contact.first_relation'''
        data = self.dict['body']['user_contact']['first_relation']
        sql = 'SELECT frist_contact_relation FROM user_info WHERE id = {0}'.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        if data2 == '1':
            data2 = '1'
        elif data2 == '2':
            data2 = '3'
        elif data2 == '3':
            data2 = '4'
        elif data2 == '4':
            data2 = '4'
        elif data2 == '5':
            data2 = '2'
        elif data2 == '6':
            data2 = '11'
        elif data2 == '7':
            data2 = '12'
        else:
            data2 = '101'
        self.assertEqual(data, data2)

    def test_73_body_user_contact_first_name(self):
        '''判断body.user_contact.first_name'''
        data = self.dict['body']['user_contact']['first_name']
        sql = 'SELECT first_contact_name FROM user_info WHERE id = {0}'.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_74_body_user_contact_first_mobile(self):
        '''判断body.user_contact.first_mobile'''
        data = self.dict['body']['user_contact']['first_mobile']
        sql = 'SELECT first_contact_phone FROM user_info WHERE id = {0}'.format(self.user_id)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_75_body_user_contact_first_is_reg(self):
        '''判断body.user_contact.first_is_reg'''
        data = self.dict['body']['user_contact']['first_is_reg']
        data1 = str(int(data))

        # 声明全局变量first_mobile
        global first_mobile
        first_mobile = self.dict['body']['user_contact']['first_mobile']
        # 此处需要加上商户号的校验,因为同一手机号可能会在不同的商户号上注册账号
        sql = 'SELECT COUNT(*) FROM user_info WHERE user_phone = {0} AND merchant_number = {1}'.format(first_mobile, self.merchant_number)
        data2 = self.db.get_one(sql=sql)
        data3 = self.is_none.is_None(data2).is_none()
        # 此处需要做校验,使用user_phone及商户号拉取用户总数,如果使用第一联系人的电话号码查询结果大于0,则表示第一联系人在本平台已注册
        data4 = int(data3)
        if data4 > 0:
            data4 = '1'
        else:
            data4 = '0'
        self.assertEqual(data1, data4)

    def test_76_body_user_contact_first_reg_info_name(self):
        '''判断body.user_contact.first_reg_info[0]name'''
        data = self.dict['body']['user_contact']['first_reg_info']['name']
        sql = 'SELECT realname FROM user_info WHERE user_phone = {0} AND merchant_number = {1}'.format(first_mobile, self.merchant_number)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_77_body_user_contact_first_reg_info_phone(self):
        '''判断body.user_contact.first_reg_info[0]phone'''
        data = self.dict['body']['user_contact']['first_reg_info']['phone']
        sql = 'SELECT user_phone FROM user_info WHERE user_phone = {0} AND merchant_number = {1}'.format(first_mobile, self.merchant_number)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_78_body_user_contact_first_reg_info_id_number(self):
        '''判断body.user_contact.first_reg_info[0]id_number'''
        data = self.dict['body']['user_contact']['first_reg_info']['id_number']
        sql = 'SELECT id_number FROM user_info WHERE user_phone = {0} AND merchant_number = {1}'.format(first_mobile, self.merchant_number)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)

    def test_79_body_user_contact_first_reg_info_reg_time(self):
        '''判断body.user_contact.first_reg_info[0]reg_time'''
        data = self.dict['body']['user_contact']['first_reg_info']['reg_time']
        sql = 'SELECT create_time FROM user_info WHERE user_phone = {0} AND merchant_number = {1}'.format(first_mobile, self.merchant_number)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        # 此处需要转换成时间戳的形式进行断言对比
        timeArray = time.strptime(data2, "%Y-%m-%d %H:%M:%S")
        reg_time = str(int(time.mktime(timeArray)))
        self.assertEqual(data, reg_time)

    def test_80_body_user_contact_first_reg_info_reg_ip(self):
        '''判断body.user_contact.first_reg_info[0]reg_ip'''
        data = self.dict['body']['user_contact']['first_reg_info']['reg_ip']
        sql = 'SELECT create_ip FROM user_info WHERE user_phone = {0} AND merchant_number = {1}'.format(first_mobile, self.merchant_number)
        data1 = self.db.get_one(sql=sql)
        data2 = self.is_none.is_None(data1).is_none()
        self.assertEqual(data, data2)


if __name__ == '__main__':
    unittest.main()




