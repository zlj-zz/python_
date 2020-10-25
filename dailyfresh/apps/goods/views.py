from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.views.generic import View
from django.core.cache import cache
from django_redis import get_redis_connection

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner, GoodsSKU
from order.models import OrderGoods

# Create your views here.


# http://127.0.0.1:8000
class IndexView(View):
    def get(self, request):
        '''首页'''

        # todo: 尝试从缓存拿数据
        context = cache.get('index_page_data')
        if context is None:

            # todo: 获取商品种信息
            types = GoodsType.objects.all()

            # todo: 获取轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')

            # todo: 获取促销活动信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by(
                'index')

            # todo: 获取分类商品信息
            for type in types:
                # todo: 获取type种类首页分类商品图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(
                    type=type, display_type=1).order_by('index')
                # todo: 获取type种类首页分类商品展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(
                    type=type, display_type=0).order_by('index')

                type.image_banners = image_banners
                type.title_banners = title_banners

            context = {
                'types': types,
                'goods_banners': goods_banners,
                'promotion_banners': promotion_banners,
            }

            # 设置缓存
            cache.set('index_page_data', context, 3600)

        # 获取购物车中商品数
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        context.update(cart_count=cart_count)

        return render(request, 'index.html', context)


class DetailView(View):
    '''详情页'''
    def get(self, request, goods_id):
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 获取商品分类信息
        types = GoodsType.objects.all()

        #  获取商品评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 获取新品推荐
        new_skus = GoodsSKU.objects.filter(
            type=sku.type).order_by('-create_time')[:2]

        # 获取同一个SPU的其他商品
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(
            id=goods_id)

        # 获取购物车中商品数
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

            # 添加用户历史浏览
            conn = get_redis_connection('default')
            history_key = 'history_%d' % user.id
            # 移除
            conn.lrem(history_key, 0, goods_id)
            # 左侧插入
            conn.lpush(history_key, goods_id)
            # 只保存最新5条数据
            conn.ltrim(history_key, 0, 4)

        context = {
            'sku': sku,
            'types': types,
            'sku_orders': sku_orders,
            'new_skus': new_skus,
            'same_spu_skus': same_spu_skus,
            'cart_count': cart_count,
        }
        return render(request, 'detail.html', context)


# id page sort
# /list/id/page/sort
class ListView(View):
    '''list'''
    def get(self, request, type_id, page):

        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 获取商品分类信息
        types = GoodsType.objects.all()

        # 获取排序方式
        sort = request.GET.get('sort')
        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort = 'default'
            # 获取分类商品信息
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')

        # 对数据进行分页
        paginator = Paginator(skus, 2)
        # 获取页码
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        skus_page = paginator.page(page)

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

        # 获取新品推荐
        new_skus = GoodsSKU.objects.filter(
            type=type).order_by('-create_time')[:2]

        # 获取购物车中商品数
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        context = {
            'type': type,
            'types': types,
            'skus_page': skus_page,
            'new_skus': new_skus,
            'cart_count': cart_count,
            'pages': pages,
            'sort': sort,
        }

        return render(request, 'list.html', context)
