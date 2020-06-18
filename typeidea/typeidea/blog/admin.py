from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [
        PostInline,
    ]

    list_display = ('name', 'status', 'is_nav', 'created_time') # 展示项
    fields = ('name', 'status', 'is_nav') # 选择项

    def post_count(self, obj):
        """TODO: Docstring for post_count.

        :obj: TODO
        :returns: TODO

        """
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户的分类. """

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        """TODO: 返回要展示的内容和查询用的 id.

        :request: TODO
        :model_admin: TODO
        :returns: TODO

        """
        return Category.objects.filter(owner=request.user).values_list(
            'id', 'name')

    def queryset(self, requsert, queryset):
        """TODO: 根据 URL Query 的内容返回列表数据.

        :requsert: TODO
        :queryset: TODO
        :returns: TODO

        """
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    """Docstring for PostAdmin. """

    form = PostAdminForm

    list_display = [
        'title', 'category', 'status', 'created_time', 'owner', 'operator'
    ]
    list_display_links = []

    # list_filter = ['category']
    list_filter = [
        CategoryOwnerFilter,
    ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        }),
    )

    filter_horizontal = ('tag', )

    # class Media:
    # css = {
    # 'all':
    # ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
    # )
    # }
    # js = (
    # 'https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',
    # )

    def operator(self, obj):
        """TODO: Docstring for operator.

        :obj: TODO
        :returns: TODO

        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id, )))

    operator.short_description = "操作"


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_repr', 'object_id', 'action_flag', 'user', 'change_message'
    ]
