# -*- coding:UTF-8 -*-
"""Base Admin

File Name: base_admin.py
Last Modified: 
Created Time: 2020-06-16


"""

__author__ = 'zachary'

from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """Docstring for BaseOwnerAdmin.

    1. 用来自动补充文章、分类、标签、侧边栏、友链这些 Model 的 owner 字段
    2. 用来针对 queryset 过滤当前用户的数据

    """

    exclude = ('owner', )

    def get_queryset(self, request):
        """TODO: Docstring for get_queryset.

        :request: TODO
        :returns: TODO

        """
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        """TODO: Docstring for save_model.

        :request: TODO
        :obj: TODO
        :form: TODO
        :change: TODO
        :returns: TODO

        """
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form,
                                                      change)
