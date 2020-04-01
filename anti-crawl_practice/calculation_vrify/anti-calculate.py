#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'zachary'
"""
File Name: anti-calculate.py
Created Time: 2020-04-01 17:59:17
Last Modified: 
"""

import os
import time
import re
from selenium import webdriver
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image


def save_verify_img(browser, id):
    """
    Save the verification code picture in the current directory.
    :param: browser
    :param: id
    return: verify_code
    """
    verify_img = browser.find_element_by_id(id)
    # Get the coordinates of the specified label
    left = verify_img.location['x']
    top = verify_img.location['y']
    right = verify_img.location['x'] + verify_img.size['width']
    bottom = verify_img.location['y'] + verify_img.size['height']

    browser.save_screenshot("screenshot.png")
    im = Image.open('screenshot.png')
    # crop entire screenshot to get target image
    im = im.crop((left, top, right, bottom))
    verify_code = 'verify_code.png'
    im.save(verify_code)

    return verify_code


def handler(grays, threshold=160):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    anti = grays.point(table, '1')

    return anti


def operator_func(a: int, b: int, oper: str) -> int:
    """
    return calculate result.
    :param: a
    :param: b
    return: 
    """
    if oper == '+':
        return a + b
    elif oper == '-':
        return a - b
    elif oper == '*':
        return a * b


if __name__ == "__main__":
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false});'

    dir = os.getcwd()
    path = os.path.join(dir, "html/calcu.html")
    url = "file://" + path

    browser = webdriver.Firefox(executable_path='../geckodriver')
    browser.get(url)
    browser.execute_script(script)
    time.sleep(1)

    code_img = save_verify_img(browser, 'matchesCanvas')
    # grayscale processing
    gray = Image.open(code_img).convert('L')
    # image binarization
    image = handler(gray)
    strings = pytesseract.image_to_string(image)
    print(strings)
    # get number and operator
    string = re.findall(r'\d+', strings)
    operator = re.findall(r'[+|\-|\*]', strings)

    result = operator_func(int(string[0]), int(string[1]), operator[0])

    input_code = browser.find_element_by_id('code')
    input_code.sendKeys(result)
    bt = browser.find_element_by_id('bt')
    bt.click()

    time.sleep(1)

    content = browser.page_source
    print(content)
    browser.quit()
