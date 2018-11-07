#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 18:46
# @Author  : Weiqiang.long
# @Site    : 
# @File    : run_all.py
# @Software: PyCharm

import os
import time
import unittest
from HTMLTestRunnerPY3.HTMLTestRunner_PY3 import HTMLTestRunner
# from ExtentHTMLTestRunner.ExtentHTMLTestRunner import HTMLTestRunner
from case.test import jsxjx_self_data

base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]





if __name__ == '__main__':

    # 获取时间，以时间命名报告
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    report_name = "result" + now + ".html"

    # 定义报告存放路径
    report_file = base_path + "\\report\\{0}".format(report_name)

    report_title = 'xjx-风控自有数据接口测试执行报告'
    desc = 'python3.7+requests'

    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.makeSuite(jsxjx_self_data))

    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner(stream=report, title=report_title, description=desc)
        runner.run(testsuite)


        # runner = HTMLTestRunner(
        #     stream=report,
        #     title='自动化测试报告',
        #     description='用例执行情况：')
        # runner.run(testsuite)