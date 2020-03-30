import sys
import time
from importlib import reload
from hdfs.client import Client
import urllib.request

reload(sys)

url = 'http://localhost:50070'                                                              
client = Client(url=url)
path = "/pyhdfs/"
# p = client.resolve(path)
# print(p)
# client.makedirs(hdfs_path=path)
# l_path= "2020-03-10-23-01-4.txt"
# client.upload(hdfs_path=path, local_path=l_path)
client.download(path+"2020-03-10-23-01-4.txt", '.')
d = time.strftime("%Y-%m", time.localtime())
print(d)

urllib.request.urlretrieve()