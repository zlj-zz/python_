from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
import re

from user.models import User, Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods

from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from celery_tasks.tasks import send_register_active_mail
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection


# Create your views here.


class RegisterView(View):
    def get(self, request):
        '''显示注册界面'''
        return render(request, 'register.html')

    def post(self, request):
        '''注册处理'''
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # allow = request.POST.get('allow')

        # if not all([username, password, email]):
        #     return  render(request, 'register.html', {'errmsg': '数据不完整'})
        #
        # if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        #     return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        #
        # if allow != 'on':
        #     return render(request, 'register.html', {'errmsg': 'qingtongyi'})

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)
            user.is_active = 0
            user.save()

            # 加密用户信息
            serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user.id}
            token = serializer.dumps(info)
            token = token.decode('utf8')

            # 发送激活邮件
            send_register_active_mail.delay(email, username, token)

            return redirect(reverse('goods:index'))
        else:
            return render(request, 'register.html', {'errmsg': '用户已存在'})


class ActiveView(View):
    '''用户激活'''

    def get(self, request, token):
        # 解密用户信息
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']

            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接过期')


class LoginView(View):
    '''登录'''

    def get(self, request):
        # 判断
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ""
            checked = ""
        return render(request, 'login.html', {'username': username, 'checked': checked, })

    def post(self, request):
        '''登录校验'''
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, username]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                # 记录登录状态
                login(request, user)
                # 获取登录跳转地址
                next_url = request.GET.get('next', reverse('goods:index'))
                # 跳转首页
                response = redirect(next_url)
                # 判断是否 记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        logout(request)
        # 退出后跳转页面
        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
    '''用户中心-信息页'''

    def get(self, request):
        '''
        Django 给 request 添加 request.user
        用户登录状态 user是User实例 未登录状态user是AnonymousUser实例
        status = request.user.is_authenticated()  // user是User实例时status是True；user是AnonymousUser实例时status是False
        :param request:
        :return:
        '''

        # 获取用户信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # from redis import StrictRedis
        # StrictRedis(host='127.0.0.1', port=6379, db=9)

        # 获取用户历史浏览记录
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id
        # 获取最新浏览商品 ID
        ske_ids = con.lrange(history_key, 0, 4)
        # 从数据库查询浏览商品具体信息
        goods_li = []
        for id in ske_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        context = {
            'page': 'user',
            'address': address,
            'goods_li': goods_li,
        }

        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
    '''用户中心-订单页'''

    def get(self, request, page):
        # 获取用户订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
        #
        for order in orders:
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)
            for order_sku in order_skus:
                amount = order_sku.count * order_sku.price
                order_sku.amount = amount
            #
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            order.order_skus = order_skus
        # 分页
        paginator = Paginator(orders, 1)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        order_page = paginator.page(page)
        # 最多显示5页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)
        # todo: context
        context = {
            'order_page': order_page,
            'pages': pages,
            'page': 'order',
        }

        return render(request, 'user_center_order.html', context)


class AddressView(LoginRequiredMixin, View):
    '''用户中心-地址页'''

    def get(self, request):
        # 获取用户默认收货地址
        user = request.user
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            address = None

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):

        # 接受数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机号码格式不正确'})

        # 业务处理 地址添加
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None

        # 获取默认地址
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        return redirect(reverse('user:address'))
