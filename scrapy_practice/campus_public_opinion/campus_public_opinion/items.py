# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CampusPublicOpinionItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field() # detail page url
    title = scrapy.Field() # detail page title
    content = scrapy.Field() #
    reply_number = scrapy.Field() # total number of replies
    last_reply_time = scrapy.Field() # last reply time of post
    pass
