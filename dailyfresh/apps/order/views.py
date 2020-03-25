from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
from django_redis import get_redis_connection
from datetime import datetime
import os

from utils.mixin import LoginRequiredMixin
from goods.models import GoodsSKU
from user.models import Address
from order.models import OrderInfo, OrderGoods

from alipay import AliPay, ISVAliPay


# Create your views here.

class OrderPlaceView(LoginRequiredMixin, View):
    '''提交订单'''

    def post(self, request):
        ''''''
        user = request.user
        sku_ids = request.POST.getlist('sku_ids')
        if not sku_ids:
            return redirect(reverse('cart:show'))
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # todo:遍历信息
        skus = []
        total_count = 0
        total_amount = 0
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            count = conn.hget(cart_key, sku_id)
            amount = sku.price * int(count)
            sku.count = count
            sku.amount = amount
            skus.append(sku)
            total_count += int(count)
            total_amount += int(amount)
        # todo:运费有子系统
        transit_price = 10
        total_pay = transit_price + total_amount
        addrs = Address.objects.filter(user=user)
        # todo: 生成上下文
        sku_ids = ','.join(sku_ids)
        context = {
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'transit_price': transit_price,
            'total_pay': total_pay,
            'addrs': addrs,
            'sku_ids': sku_ids,
        }
        # todo: 使用模板
        return render(request, 'place_order.html', context)


class OrderCommitView(View):
    '''创建订单'''

    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'user not login'})
        # todo: receiver params
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')
        # todo:检验参数
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': 'incomplete parameters'})
        if pay_method not in OrderInfo.PAY_METHOD.keys():
            return JsonResponse({'res': 2, 'errmsg': 'error pay'})
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': 'address error'})

        # todo: add data to OrderInfo
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transit_price = 10
        total_count = 0
        total_amount = 0
        # set save point
        save_id = transaction.savepoint()
        try:
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user, addr=addr,
                                             pay_method=pay_method,
                                             total_count=total_count,
                                             total_price=total_amount,
                                             transit_price=transit_price)
            # todo:
            print('ok')
            sku_ids = sku_ids.split(',')
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            for sku_id in sku_ids:
                try:
                    sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': 'sku error'})
                count = conn.hget(cart_key, sku_id)
                # todo:  judge product reserve
                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 6, 'errmsg': 'product shortage'})
                # todo: add data to OrderGoods
                OrderGoods.objects.create(order=order,
                                          sku=sku,
                                          count=count,
                                          price=sku.price)
                # todo: update product reserve
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()
                # todo: compute count and amount
                total_count += int(count)
                amount = sku.price * int(count)
                total_amount += amount
            # todo: update total_count and total_amount of OrderInfo
            order.total_count = total_count
            order.total_price = total_amount
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'message': 'failure'})
        # todo: del data from shopping cart
        transaction.savepoint_commit(save_id)
        conn.hdel(cart_key, *sku_ids)
        return JsonResponse({'res': 5, 'message': 'successful'})


class OrderPay(View):
    '''订单支付'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'user not login'})
        order_id = request.POST.get('order_id')
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': 'error order'})
        way = OrderInfo.objects
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': 'error order 2'})
        print('111111')
        # 使用alipay SDK
        # 配置地址
        private_path = os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')
        public_path = os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')
        # 获取公私钥字符串
        app_private_key_string = open(private_path).read()
        alipay_public_key_string = open(public_path).read()
        alipay = AliPay(appid='2016101700711419',
                        app_notify_url=None,
                        app_private_key_string=app_private_key_string,
                        alipay_public_key_string=alipay_public_key_string,
                        sign_type='RSA2',
                        debug=True)
        total_pay = order.total_price + order.transit_price
        order_string = alipay.api_alipay_trade_page_pay(out_trade_no=order_id,
                                                        total_amount=str(total_pay),
                                                        subject='ttsx%s' % order_id,
                                                        return_url=None,
                                                        notify_url=None,

                                                        )
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res': 3, 'pay_url': pay_url})


class CheckPayView(View):
    '''获取交易结果'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'user not login'})
        order_id = request.POST.get('order_id')
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': 'error order'})

        try:

            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': 'error order 2'})
        print('111111')
        # 使用alipay SDK
        # 配置地址
        private_path = os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')
        public_path = os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')
        # 获取公私钥字符串
        app_private_key_string = open(private_path).read()
        alipay_public_key_string = open(public_path).read()
        alipay = AliPay(appid='2016101700711419',
                        app_notify_url=None,
                        app_private_key_string=app_private_key_string,
                        alipay_public_key_string=alipay_public_key_string,
                        sign_type='RSA2',
                        debug=True)
        while True:
            response = alipay.api_alipay_trade_query(out_trade_no=order_id)
            code = response.get('code')
            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                trade_no = response.get('trade_no')
                order.trade_no = trade_no
                order.order_status = 4
                order.save()
                return JsonResponse({'res': 3, 'message': 'success'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # wait
                import time
                time.sleep(5)
                continue
            else:
                return JsonResponse({'res': 4, 'errmsg': 'pay fail'})


class CommentView(LoginRequiredMixin, View):
    """订单评论"""

    def get(self, request, order_id):
        """提供评论页面"""
        user = request.user
        # 校验数据
        if not order_id:
            return redirect(reverse('user:order'))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        # 根据订单的状态获取订单的状态标题
        order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

        # 获取订单商品信息
        order_skus = OrderGoods.objects.filter(order_id=order_id)
        for order_sku in order_skus:
            # 计算商品的小计
            amount = order_sku.count * order_sku.price
            # 动态给order_sku增加属性amount,保存商品小计
            order_sku.amount = amount
        # 动态给order增加属性order_skus, 保存订单商品信息
        order.order_skus = order_skus

        # 使用模板
        return render(request, "order_comment.html", {"order": order})

    def post(self, request, order_id):
        """处理评论内容"""
        user = request.user
        # 校验数据
        if not order_id:
            return redirect(reverse('user:order'))

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return redirect(reverse("user:order"))

        # 获取评论条数
        total_count = request.POST.get("total_count")
        total_count = int(total_count)

        # 循环获取订单中商品的评论内容
        for i in range(1, total_count + 1):
            # 获取评论的商品的id
            sku_id = request.POST.get("sku_%d" % i)  # sku_1 sku_2
            # 获取评论的商品的内容
            content = request.POST.get('content_%d' % i, '')  # cotent_1 content_2 content_3
            try:
                order_goods = OrderGoods.objects.get(order=order, sku_id=sku_id)
            except OrderGoods.DoesNotExist:
                continue

            order_goods.comment = content
            order_goods.save()

        order.order_status = 5  # 已完成
        order.save()

        return redirect(reverse("user:order", kwargs={"page": 1}))
