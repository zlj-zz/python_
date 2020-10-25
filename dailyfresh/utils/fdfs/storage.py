from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    '''fastdfs文件存储类'''
    def __init__(self, client_conf=None, base_url=None):

        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        # 创建Fdfs_client对象 加载配置文件
        client = Fdfs_client(self.client_conf)

        # 上传文件到fastdfs
        res = client.upload_appender_by_buffer(content.read())

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
