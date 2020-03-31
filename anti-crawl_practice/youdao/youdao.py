#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
__author__ = 'zachary'
"""
File Name: youdao.py
Created Time: 2020年03月28日 星期六 00时07分56秒
Lnast Modified: 2020-03-28 01:07:20
"""

import time
import requests
import hashlib
import random
import json


class youdaofanyiweb():
    def __init__(self):
        """
        init parameters.
        :return
        """
        self.app_version = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'

        self.cookie = '_ga=GA1.2.1091756845.1584888050; OUTFOX_SEARCH_USER_ID_NCOO=257795495.14613608; OUTFOX_SEARCH_USER_ID="-794258332@10.169.0.83"; _gid=GA1.2.577062243.1585130778; P_INFO=13177310312|1585145091|1|youdaonote|00&99|null&null&null#not_found&null#10#0|&0|null|13177310312; JSESSIONID=aaacSJiU5zytz_pidSCex; ___rl__test__cookies=1585324538971'

        self.headers = {
            'User-Agent': self.app_version,
            'Cookie': self.cookie,
            'Host': 'fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/?keyfrom=fanyi-new.logo',
        }

        self.fanyi_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    def analyse_data(self, content, from_, to_):
        """
        encrypt data to generate target parameters.
        :return: data
        """
        bv = hashlib.md5(self.app_version.encode()).hexdigest()
        ts = time.time()
        salt = ts + random.randint(0, 9)
        client = 'fanyideskweb'
        addtional_str = 'Nw(nmmbP%A-r6U3EUn]Aj'
        sign = hashlib.md5((client + str(content) + str(salt) +
                            addtional_str).encode()).hexdigest()

        data = {
            'i': str(content),
            'from': from_,
            'to': to_,
            'smartresult': 'dict',
            'client': client,
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': bv,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }
        return data

    def process_result(self, tmp_result):
        """
        format result.
        :param data:
        :return:
        """
        tmp_result = json.loads(tmp_result)
        source = tmp_result['translateResult'][0][0]['src']
        target = tmp_result['translateResult'][0][0]['tgt']
        other = ''.join(
            [item for item in tmp_result['smartResult']['entries']])
        return source + '\t' + target + '\r\n' + other

    def translate(self, content, from_='AUTO', to_='AUTO'):
        """
        automatic translation by default, can spcify by parameter 'from_' and 'to_'.
        :param content:
        :param from_:
        :param to_:
        :return: result
        """
        response = requests.post(self.fanyi_url,
                                 data=self.analyse_data(content, from_, to_),
                                 headers=self.headers)
        tmp_result = response.content.decode()
        result = self.process_result(tmp_result)
        return result


if __name__ == '__main__':
    # content = 'current'
    content = input('input what you want to translate:')
    ydfy = youdaofanyiweb()
    result = ydfy.translate(content)
    print(result)
