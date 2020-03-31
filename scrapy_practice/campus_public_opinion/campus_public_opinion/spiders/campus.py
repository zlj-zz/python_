# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from campus_public_opinion.items import CampusPublicOpinionItem


class CampusSpider(CrawlSpider):
    name = 'campus'
    allowed_domains = ['baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=%BA%FE%B1%B1%C0%ED%B9%A4%D1%A7%D4%BA']

    regx = r'class="threadlist_title pull_left j_th_tit ".*?rel="noreferrer".*?href="(.*?)"'
    rules = (
        Rule(LinkExtractor(allow=regx), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = CampusPublicOpinionItem()
        # print(response)
        item['title'] = response.xpath('//div[@class="core_title core_title_theme_bright"]/h1/@title').get()
        print(item["title"])
        print("dfsaadsfsadf ")
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
