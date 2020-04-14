# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time
import sys
from importlib import reload
from hdfs.client import Client
from campus_public_opinion.settings import HDFS_URL
# import json


class CampusPublicOpinionPipeline(object):
    def __init__(self):
        """
        Create storage folder
        Create file stream
        """
        dir = os.path.abspath('.') + "/tieba"
        if not os.path.exists(dir):
            os.mkdir(dir)
        file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".csv"
        self.file_path = dir + "/" + file_name
        print(self.file_path)
        self.fp = open(self.file_path, mode='w+')

    def process_item(self, item, spider):
        """
        Save file
        :param item:
        :param spider:
        :return:
        """
        print(item)
        # print(type(item))
        # json.dump(dict(item), self.fp, ensure_ascii=False, indent=2)
        txt = item["url"] + '\t' + item["title"] + '\t' + item[
            "reply_number"] + '\t' + item["last_reply_time"] + '\t' + item[
                "content"]
        self.fp.write(txt)
        self.fp.write("\r\n")
        return item

    def close_spider(self, spider):
        """
        Close file stream, upload data to hdfs
        :param spider:
        :return:
        """
        self.fp.close()
        # reload(sys)
        # client = Client(url=HDFS_URL)
        # d = time.strftime("%Y-%m", time.localtime())
        # path = "/pyhdfs/" + d
        # client.makedirs(hdfs_path=path)
        # # l_path = "2020-03-10-23-01-4.txt"
        # client.upload(hdfs_path=path, local_path=self.file_path)
        # print("upload ok")
        pass


"""
hive> create table cpo_1 (url string, title string, reply_number int, last_time string, content array<string>)
    > row format delimited fields terminated by '\t' collection items terminated by '|';
"""
