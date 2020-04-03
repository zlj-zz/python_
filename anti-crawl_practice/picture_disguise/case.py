#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'zachary'
"""
File Name: case.py
Created Time: 2020-04-03 17:08:31
Last Modified: 
"""

import io
import os
import requests
from parsel import Selector
from urllib.parse import urljoin
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

if __name__ == "__main__":
    dir = os.getcwd()
    path = os.path.join(dir, 'html/pd.html')
    url = 'file://' + path

    # response_ = requests.get(url)  # when request network resources
    response_ = open('./html/pd.html').read()
    # print(response_)
    sel = Selector(response_)

    image_name = sel.css('.pn::attr("src")').extract_first()
    image_url = urljoin(url, image_name)
    # print(image_url)

    # image_body = requests.get(image_url).content()  # when request network resources
    image_body = open('./html/phonenumber.png', 'rb').read()
    image_stream = Image.open(io.BytesIO(image_body))
    print(pytesseract.image_to_string(image_stream))
