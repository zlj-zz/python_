#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'zachary'
"""
File Name: case.py
Created Time: 2020-04-04 19:32:10
Last Modified: 
"""

import requests
import os
import re
from parsel import Selector

if __name__ == "__main__":
    # url = ''
    # resp = requests.get(url)
    resp = open('./html/flight.html').read()

    sel = Selector(resp)
    em = sel.css('em.rel').extract()

    for element in em:
        element = Selector(element)
        element_b = element.css('b').extract()
        bl = Selector(element_b.pop(0))
        bl_style = bl.css('b::attr("style")').get()
        bl_width = ''.join(re.findall('width:(.*?)px', bl_style))
        number = int(int(bl_width) / 16)
        base_price = bl.css('i::text').extract()
        base_price = bl.css('i::text').extract()[:number]

        alternate_price = []
        for eb in element_b:
            eb = Selector(eb)
            style = eb.css('b::attr("style")').get()
            position = ''.join(re.findall('left:(.*?)px', style))
            value = eb.css('b::text').get()
            alternate_price.append({'position': position, 'value': value})

        for al in alternate_price:
            position = int(al.get('position'))
            value = al.get('value')
            plus = True if position >= 0 else False
            index = int(position / 16)
            # replace
            base_price[index] = value
        print(base_price)
