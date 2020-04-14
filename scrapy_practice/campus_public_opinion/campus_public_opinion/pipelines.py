# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time
import pymysql
import sys
from importlib import reload
# from hdfs.client import Client
from campus_public_opinion.settings import HDFS_URL
# import json


class CampusPublicOpinionPipeline(object):
    def __init__(self):
        """
        Create mysql connect and create saving table
        :return:
        """
        self.username = 'root'
        self.password = 'mysql'
        self.url = '127.0.0.1'
        self.port = 3306
        self.database = 'campus'
        self.conn = pymysql.connect(self.url,
                                    port=self.port,
                                    database=self.database,
                                    user=self.username,
                                    password=self.password)
        self.cursor = self.conn.cursor()
        self.table_name = 'campus_' + time.strftime("%Y_%m_%d_%H_%M_%S",
                                                    time.localtime())
        sql = '''CREATE TABLE {}(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(100),
            url VARCHAR(100),
            last_reply_time VARCHAR(10),
            reply_num INT,
            content TEXT
        )CHARSET utf8mb4'''.format(self.table_name)
        print(sql)
        self.cursor.execute(sql)

    def process_item(self, item, spider):
        """
        Save file to mysql
        :param item:
        :param spider:
        :return:
        """
        print(item)
        sql = '''INSERT INTO {} (title, url, last_reply_time, reply_num, content)VALUES('{}','{}','{}',{},'{}')'''.format(
            self.table_name,
            item['title'], item['url'], item['last_reply_time'],
            int(item['reply_number']), item['content'])
        print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        """
        Close mysql connect, upload data to HDFS
        :param spider:
        :return:
        """
        reload(sys)
        self.cursor.close()
        self.conn.close()
        # sql = 'select * from' + self.table_name
        # target_dir = '/tmp/jbw/sqoop_data/'
        # sqoop = '''
        # sqoop import --username {} --password {} --connect jdbc:mysql://{}:{}/{} --query "{} where \$CONDITIONS" \
        # --target-dir {} --fields-terminated-by ',' --split-by id -m 1
        # '''.format(self.username, self.password, self.url, self.port, self.database, sql, target_dir)
        # os.system(sqoop)
        print("upload ok")


"""

hive> CREATE EXTERNAL TABLE IF NOT EXISTS cpo (
    > url string, 
    > title string, 
    > reply_number int, 
    > last_time string, 
    > content array<string>
    > )row format delimited fields terminated by '\t'
    > collection items terminated by '|';
        
"""
'''

select * from cpo order by reply_num desc limit 1;

'''
