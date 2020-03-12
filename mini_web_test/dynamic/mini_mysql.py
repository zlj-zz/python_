# coding=utf-8

from pymysql import connect

class MiniMysql(object):
    """docstring for MiniMysql"""
    def __init__(self, host, port, user, password, database):
        super(MiniMysql, self).__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.conn = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, charset='utf8')
        self.cs = self.conn.cursor()
        return self.cs
        
    def close(self):
        self.cs.close()
        self.conn.close()

    def select_all(self, sql):
        cs = self.connect()
        cs.execute(sql)
        info =  cs.fetchall()
        self.close()
        return info

    def add_follow(self, sql):
        pass

    def del_follow(self, sql):
        pass

    def update_remark(self, sql):
        pass
