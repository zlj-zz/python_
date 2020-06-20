# -*- coding:UTF-8 -*-
"""

File Name: sitemap.py
Last Modified: 
Created Time: 2020-06-21


"""

__author__ = 'zachary'

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    """Docstring for PostSitemap. """

    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('post-detail', args=[obj.pk])
