import requests
from lxml import etree
import time
import os


class TiebaSpider(object):
    """docstring for TiebaSpider"""

    def __init__(self, tieba_name):
        self.headers = {  # 请求头
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        }
        self.params = {  # get参数
        }
        # 初始url地址
        self.url_temp = "http://tieba.baidu.com"
        self.name = tieba_name
        self.session = requests.session()

    def get_first_level_url_list(self):
        """默认只抓取最新的前五页"""
        url = self.url_temp + "/f?ie=utf-8&pn={}&kw=" + self.name
        url_list = []
        for i in range(5):
            url_list.append(url.format(i * 50))
        return url_list

    def get_second_level_url_list(self):
        # self.a = 10
        # if (a = self.a -1):
        #     print("ok")
        pass

    def parse_url(self, url):
        """获取网页源码"""
        response = requests.get(url, headers=None)
        return response.content

    def extract_data(self, html_code):
        """xpath解析数据,提取：标题、发贴人、内容、具体帖子url"""
        xpath_str = etree.HTML(html_code)
        div_list = xpath_str.xpath("//div[@class='t_con cleafix']//div[contains(@class,'col2_right')]")
        content_list = list()  # 存放数据的list
        #
        for div in div_list:
            title = div.xpath(".//div[contains(@class,'threadlist_title')]/a/text()")[0]
            # print(title)
            frs_author = div.xpath(".//span[@class='frs-author-name-wrap']/a/text()")[0]
            # print(frs_author)
            content = div.xpath(".//div[contains(@class,'threadlist_abs')]/text()")
            content = content[0].replace("\n", "") if len(content) > 0 else ""
            # print(content)
            detail_url = div.xpath(".//div[contains(@class,'threadlist_title')]/a/@href")
            detail_url = self.url_temp + detail_url[0]
            # print(detail_url)
            # print("************************************************")
            content_list.append(title + ":" + frs_author + "\r\n" + content + "\r\n" + detail_url)
        return content_list

    def save_to_txt(self, content_list):
        path = '/home/zachary/Projects/campus_public_opinion/tieba.txt'
        if not os.path.exists(path):
            pass
        # print(content_list)
        with open(path, "a") as f:
            for content in content_list:
                f.write(content)
                f.write("\r\n\r\n\r\n")

    def run(self):
        url_list = self.get_first_level_url_list()
        for url in url_list:
            html_code = self.parse_url(url)
            content_list = self.extract_data(html_code)
            self.save_to_txt(content_list)
            time.sleep(3)


if __name__ == '__main__':
    # t = TiebaSpider("湖北理工学院")
    # t.run()
    # print(os.path.abspath("../..")+"/tieba")
    a = 10
    a -= 1
    # if (a:=1) >0:
    #     print(a)

# 带headers不行