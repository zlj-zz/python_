# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SuningBookPipeline(object):
    list = []

    def process_item(self, item, spider):
        SuningBookPipeline.list.append(item)
        if len(SuningBookPipeline.list) > 200:
            self.write_file(SuningBookPipeline.list)
            SuningBookPipeline.list.clear()
        # print(str(item))
        return item

    def write_file(self, list):
        # print(list)
        with open("book.txt", "a") as f:
            for i in list:
                f.write(str(i))
                f.write("\r\n")
