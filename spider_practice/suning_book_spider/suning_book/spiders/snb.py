# -*- coding: utf-8 -*-
# 土屋あさみ
import scrapy
from suning_book.items import SuningBookItem
import re


class SnbSpider(scrapy.Spider):
    name = 'snb'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/1-502320-0.html']

    def parse(self, response):
        # items = SuningBookItem()
        classifications = response.xpath(
            "//div[@id='search-path']//dd//a/@href").extract()
        classification_urls = ["https:" + i for i in classifications]
        # yield scrapy.Request(
        #     classification_urls[0],
        #     callback=self.parse_one_class,
        # )
        for classification_url in classification_urls:
            # print(classification_url)
            yield scrapy.Request(
                classification_url,
                callback=self.parse_one_class,
            )

    def parse_one_class(self, response):  # 处理分类

        li_list = response.xpath(
            "//div[@id='filter-results']//ul//li[contains(@class,'book')]")
        current_page = re.findall(r"^\d-\d{6}-(\d+)",
                                  response.url.split("/")[-1])[0]
        for li in li_list:
            item = SuningBookItem()
            item["title"] = li.xpath(
                ".//p[@class='sell-point']/a/text()").extract_first()
            item["shop_name"] = li.xpath(
                ".//p[contains(@class,'seller')]/a/text()").extract_first()
            item["href"] = "http:" + li.xpath(
                ".//p[@class='sell-point']/a/@href").extract_first()
            item["page"] = current_page
            # items["price"] = li.xpath(".//p[@class='prive-tag']/em/text()").extract()
            # print(items["title"])
            # print(items["href"])
            # print(items["shop_name"])
            yield item

        # current_page = response.xpath("//div[@id='bottom_pager']/a[@class='cur']/@pagenum").extract_first()
        next_page = int(current_page) + 2
        next_url = response.xpath("//div[@id='bottom_pager']/a[@pagenum=" +
                                  str(next_page) + "]/@href").extract_first()
        print(int(current_page) + 1)
        print(response.url)
        if next_url is not None:
            yield scrapy.Request("https://list.suning.com" + next_url,
                                 callback=self.parse_one_class)
        # print(next_url)
