import pymysql
import matplotlib
import matplotlib.pyplot as plt
from  matplotlib import font_manager
import pandas as pd
import numpy as np
import jieba
import jieba.analyse as analyse

username = 'root'
password = 'mysql'
url = '127.0.0.1'
port = 3306
database = 'campus'
conn = pymysql.connect(url, port=port, database=database, user=username, password=password)
cursor = conn.cursor()
table_name = 'campus_2020_04_13_10_08_31'

# sql = 'select reply_num from {}'.format(table_name)
sql = 'select title from {}'.format(table_name)
cursor.execute(sql)
list = cursor.fetchall()
l = pd.DataFrame(list)
ll = []
for i in l[0]:
    l = analyse.extract_tags(i, topK=2, withWeight=False, allowPOS=(), withFlag=False)
    # print(l)
    ll.extend(l)

print(ll)
print(len(ll))

lld = pd.DataFrame(ll, columns=['title'] )
lla = pd.DataFrame([1 for _ in range(len(lld))], columns=['count'])
llf = pd.concat([lld, lla], axis=1)
# print(llf)

lldd = llf.groupby('title').count()
lt = lldd.sort_values(by='count')[-20:]
print(lt)
title = lt.index
print(title)
data = lt['count']

my_font = font_manager.FontProperties(fname='/usr/share/fonts/noto-cjk/NotoSansCJK-Light.ttc')

# 支持中文
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

ps = plt.bar(title, data, label='', align='center')
# for p in ps[1]:
#     p.set_fontproperties(my_font)
plt.xlabel('Hot Words')
plt.xticks(rotation=90)
plt.ylabel('Number')
plt.title('Hot-Graph')
plt.show()


print(type(lldd))


# jieba.analyse.extract_tags(sentence, topK=3, withWeight=False, allowPOS=(), withFlag=False)
# topK 表示返回最大权重关键词的个数，None表示全部
# withWeight表示是否返回权重，是的话返回(word,weight)的list
# allowPOS仅包括指定词性的词，默认为空即不筛选。
# jieba.analyse.textrank(self, sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'), withFlag=False)
# 与TF-IDF方法相似，但是注意allowPOS有默认值，即会默认过滤某些词性。

# bins = [i for i in range(0,200,10)]
# print(bins)
# plt.hist(l[0], bins, histtype='bar')
# plt.show()

# for i in list:
#     print(i[0])
#     print(type(i[0]))
# print(list)