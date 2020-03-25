from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 创建Celery实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner


# 定义任务函数
@app.task
def send_register_active_mail(to_mail, username, token):
    '''发送激活邮件'''
    print('------ start ------')
    subject = '天天生鲜欢迎您的加入'
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_mail]
    html_message = '<h1>%s,欢迎您成为我们的会员</h1><br>点击下面链接激活账户<br><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    print('send mail ------- ok')


@app.task
def generate_static_index_html():
    ''''''
    # 获取商品种信息
    types = GoodsType.objects.all()

    # 获取轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取分类商品信息
    for type in types:
        # 获取type种类首页分类商品图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        type.image_banners = image_banners
        type.title_banners = title_banners

    # 获取购物车中商品数

    context = {
        'types': types,
        'goods_banners': goods_banners,
        'promotion_banners': promotion_banners,
    }

    # 加载模板文件
    temp = loader.get_template('static_index.html')
    # 模板渲染
    static_index_html = temp.render(context)

    # 生成首页静态页面
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)

    print('static_index----------ok')
