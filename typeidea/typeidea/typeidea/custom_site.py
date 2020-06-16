# -*- coding:UTF-8 -*-
"""Custom site

File Name: custom_site.py
Last Modified: 
Created Time: 2020-06-16


"""

__author__ = 'zachary'

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    """Docstring for CustomSite. """

    site_header = 'Typeidea'
    site_title = 'Typeidea 管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
