# -*- coding: UTF-8 -*-
"""
    @program: utils
    @filename: mysql
    @author: codetiger
    @create: 2022/8/27 11:02
"""
import pymysql
from sqlalchemy import create_engine
from .log import log

class mysql:
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        # 建立数据库连接
        self.c = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            use_unicode=True,
            charset='utf8')
        # 获取游标对象
        self.cus = self.c.cursor()

    # 创建数据库引擎
    def create_engine(self):
        engine = create_engine('mysql+pymysql://' + mysql.Database("user") + ':' + mysql.Database("passwd") + '@' + mysql.Database("host") + ':' + mysql.Database("port") + '/' + mysql.Database("database") + '?charset=utf8', max_overflow=5)
        return engine

    # 获取查询结果集
    def select_all(self, sql):
        try:
            self.cus.execute(sql)
            return self.cus.fetchall()
        except Exception as e2:
            self.c.rollback()
            log.error(e2)
            log.error("插入失败")
            raise

    # 执行SQL语句，并返回数量
    def execute(self, sql):
        try:
            result = self.cus.execute(sql)
            self.c.commit()
            return result
        except Exception as e3:
            self.c.rollback()
            log.error(e3)
            log.error("执行失败")
            raise

    # 批量执行SQL语句，并返回数量
    def executes(self, sql, ll):
        self.cus = self.c.cursor()
        try:
            result = self.cus.executemany(sql, ll)
            self.c.commit()
            return result
        except Exception as e4:
            self.c.rollback()
            log.error(e4)
            log.error("执行失败")
            raise

    # 关闭数据库连接
    def close(self):
        self.cus.close()
