# coding:utf-8

from celery import Celery
from ihome.libs.yuntongxun.sms import CCP

# 定义对象
celery_app = Celery("ihome", broker="redis://127.0.0.1:6379/1")
Celery()


@celery_app.task
def send_sms(to, datas, temp_id):
    """异步发送短信"""
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)
