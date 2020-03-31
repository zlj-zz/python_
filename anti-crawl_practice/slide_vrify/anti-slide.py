#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'zachary'
"""
File Name: anti-slide.py
Created Time: 2020-03-31 19:56:42
Last Modified: 
"""

from selenium import webdriver
import time
import os

browser = webdriver.Firefox(executable_path='../geckodriver')
# open case web page
dir = os.getcwd()
path_ = os.path.join(dir, 'html/slide.html')
browser.get(url='file://' + path_)
# positioning slider
hover = browser.find_element_by_css_selector('.hover')

action = webdriver.ActionChains(browser)
action.click_and_hold(hover).perform()
action.move_by_offset(340, 0)
action.release().perform()

time.sleep(1)

botton = browser.find_element_by_id('bt')
botton.click()

content = browser.page_source
print(content)
time.sleep(1)
browser.quit()
