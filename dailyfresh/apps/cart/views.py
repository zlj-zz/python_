from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from utils.mixin import LoginRequiredMixin
from goods.models import GoodsSKU

# Create your views here.


# /cart/add
class CartAddView(View):
    '''购物车记录添加'''
    def post(self, request):
        '''append'''
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'please login'})
        # todo: 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # todo: 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': 'incomplete data'})
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': 'product number error'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': 'product does not exist'})
        # todo: 业务处理
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            count += int(cart_count)
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': 'inventory shortage'})
        conn.hset(cart_key, sku_id, count)
        total_count = conn.hlen(cart_key)
        # todo: 返回
        return JsonResponse({
            'res': 5,
            'total_count': total_count,
            'message': 'added successfully'
        })


class CartInfoView(LoginRequiredMixin, View):
    '''cart info page'''
    def get(self, request):
        # todo: get info
        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_dict = conn.hgetall(cart_key)
        # todo: traversal cart_dict
        skus = []
        tatol_count = 0
        tatol_price = 0
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            amount = sku.price * int(count)
            sku.count = count
            sku.amount = amount
            skus.append(sku)
            tatol_count += int(count)
            tatol_price += amount
        context = {
            'skus': skus,
            'tatol_count': tatol_count,
            'tatol_price': tatol_price,
        }

        return render(request, 'cart.html', context)


# cart/update
class CartUpdateView(View):
    '''cart info update'''
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'please login'})
        # todo: 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # todo: 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': 'incomplete data'})
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': 'product number error'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': 'product does not exist'})
        # todo:
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': 'inventory shortage'})
        conn.hset(cart_key, sku_id, count)
        # todo:
        tatal_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            tatal_count += int(val)
        # todo: 返回
        return JsonResponse({
            'res': 5,
            'total_count': tatal_count,
            'message': 'update successfully'
        })


class CartDeleteView(View):
    ''''''
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': 'please login'})
        # receive parameters
        sku_id = request.POST.get('sku_id')
        #
        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': 'incomplete id'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': 'product does not exist'})

        # todo: 业务处理
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        conn.hdel(cart_key, sku_id)
        # todo:
        tatal_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            tatal_count += int(val)
        # todo: 返回
        return JsonResponse({
            'res': 3,
            'total_count': tatal_count,
            'message': 'delete successfully'
        })
