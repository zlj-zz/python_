# -*- coding: utf-8 -*-
import re
from functools import reduce

import scrapy
from lxml import etree

from campus_public_opinion.items import CampusPublicOpinionItem
from .. import settings


class CampusSpider(scrapy.Spider):
    name = 'campus_'
    allowed_domains = ['baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=' + settings.CAMPUS_NAME]
    crawl_page = 10 # number of pages crawled

    def parse(self, response):
        """
        Parse list page, get details page list
        :param response:
        :return:
        """
        item = CampusPublicOpinionItem()
        content = response.text
        regx_list = r'class="threadlist_title pull_left j_th_tit ".*?rel="noreferrer".*?href="(.*?)".*?class="threadlist_reply_date pull_right j_reply_data".*?>(.*?)<'
        list = re.findall(regx_list, content, re.S)
        for l in list:
            detail_url = "http://tieba.baidu.com/" + l[0]
            item["url"] = detail_url
            last_reply_time = l[1].strip()
            item["last_reply_time"] = last_reply_time
            yield scrapy.Request(
                detail_url,
                callback=self.parse_detail,
                meta={"item": item.deepcopy()},
            )
        regx_next = r'href="(.*?)" class="next'
        next_page_url = re.findall(regx_next, content)
        next_page_url = "http:" + next_page_url[0] if next_page_url else None
        if self.crawl_page > 0:
            print(self.crawl_page, '*' * 155)
            self.crawl_page -= 1
            yield scrapy.Request(
                next_page_url,
                callback=self.parse,
            )
        else:
            return

    def parse_detail(self, response):
        """
        Parse detail page, get demand content
        :param response:
        :return:
        """
        item = response.meta["item"]
        title = response.xpath(
            '//div[@class="core_title core_title_theme_bright"]/h1/@title'
        ).extract()
        item["title"] = title[0] if title else ""
        reply_number = response.xpath(
            '//ul[@class="l_posts_num"]/li[@class="l_reply_num"]/span/text()'
        ).extract()
        item["reply_number"] = reply_number[0] if reply_number else 0
        contents = response.xpath(
            '//div[contains(@class,"l_post j_l_post")]').extract()
        # print(contents[0])
        # last_reply_time = etree.HTML(contents[0]).xpath(
        #     '//ul[@class="p_tail"]//span/text()')
        # print(last_reply_time)
        # item['last_reply_time'] = last_reply_time
        content = ""
        for comment in contents:
            comment = etree.HTML(comment)
            comment_user = comment.xpath(
                '//div[@class="d_author"]/ul/li[@class="d_name"]/a/text()')[0]
            comment_content = comment.xpath(
                '//div[contains(@class,"d_post_content_main")]/div/cc/div[contains(@class,"d_post_content")]/text()'
            )
            comment_content = [i.strip() for i in comment_content if i]
            comment_str = reduce(lambda x, y: x + y, comment_content)
            content = content + comment_user + ":" + comment_str + "|"
            content = content.replace('"', ' ').replace("'", " ")
        item["content"] = content
        yield item
        pass
