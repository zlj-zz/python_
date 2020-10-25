# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf0708701429c0017015a985ca0127'

# 主帐号Token
accountToken = '9aead7e2c7444535a2dde045173d5665'

# 应用Id
appId = '8aaf0708701429c0017015a9863c012e'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id


class CCP(object):
    """自己封装的发短信辅助类"""
    # save object
    instance = None

    def __new__(cls, *args, **kwargs):
        # 判断对象是否创建
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance

    def send_template_sms(self, to, datas, tempId):
        # 初始化REST SDK
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        status_code = result.get("statusCode")
        # print status_code == "000000"
        if status_code == "000000":
            # 表示发送短信成功
            return 0
            # print("ok")
        else:
            # 发送失败
            return -1
        # print("ok2")


if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("18162901916", ["5234", '5'], 1)
