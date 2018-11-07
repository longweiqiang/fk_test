#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 11:33
# @Author  : Weiqiang.long
# @Site    : 
# @File    : dbconfig.py
# @Software: PyCharm

from utils.config import IniConfig
import pymysql



class dbHandle():

    def __init__(self, dbname):
        db = IniConfig()
        host = db.get(dbname, 'host')
        port = int(db.get(dbname, 'dbport'))
        user = db.get(dbname, 'user')
        passwd = db.get(dbname, 'password')
        dbname = db.get(dbname, 'database')
        try:
            self.conn = pymysql.conn = pymysql.connect(host = host,
                       port = port,
                       user = user,
                       passwd = passwd,
                       db = dbname,
                       charset = 'utf8')
        except:
            print("连接数据库失败")
        self.cur = self.conn.cursor()

    def dbClose(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()

    def dbQueryLinks(self,sql):
        link_list = []
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data
    def dbInsert(self, sql):
        try:
            self.cur.execute(sql)
            print("插入成功！！！")
            self.conn.commit()

        except Exception as e:
            print(e)
            print('插入失败！！！')

    def dbUpdate(self, sql):
        try:
            self.cur.execute(sql)
            print("更新状态成功！！！")
            self.conn.commit()

        except Exception as e:
            print(e)
            print('更新状态失败！！！')

    def get_one(self, sql):
        self.cur.execute(sql)
        res = self.cur.fetchone()
        self.cur.close()
        return res


if __name__ == '__main__':
    dbHandle = dbHandle('DB')
    a = dbHandle.get_one('SELECT apr FROM asset_borrow_order where id = 50108589 ')

    print(a)
    print(type(a))








