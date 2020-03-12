# coding:utf-8

from fdfs_client.client import Fdfs_client
from ihome import constants
from ihome.models import User


class FDFSStorage(object):
    '''fastdfs文件存储类'''

    def __init__(self, client_conf=None, base_url=None):

        if client_conf is None:
            client_conf = constants.FDFS_SETTING_PATH
        self.client_conf = client_conf

        if base_url is None:
            base_url = constants.FDFS_URL
        self.base_url = base_url

    def open(self, name, mode='rb'):
        pass

    def save(self, name, content):
        # 创建Fdfs_client对象 加载配置文件
        client = Fdfs_client(self.client_conf)

        # 上传文件到fastdfs
        res = client.upload_appender_by_buffer(content)
        # res = client.upload_appender_by_buffer(content.read())
        # res = client.upload_appender_by_filename(name)
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fastdfs失败')

        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        '''判断文件名是否可用'''
        return False

    def url(self, name):
        '''返回访问url'''
        return self.base_url + name


if __name__ == "__main__":
    dfs = FDFSStorage()
    file_name = dfs.save(name='/home/zlj/Pictures/异步1.png', content=None)
    print file_name
# http://127.0.0.1:8888/group1/M00/00/00/fwAAAV48CxWEFx3vAAAAAJsCqp8976.png
