# -*- coding:UTF-8 -*-
"""

File Name: rss.py
Last Modified: 
Created Time: 2020-06-20


"""

__author__ = 'zachary'

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


class ExtendeRSSFeed(Rss201rev2Feed):
    """Docstring for ExtendeRSSFeed. """
    def add_item_elements(self, handler, item):
        super(ExtendeRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    """Docstring for LatestPostFeed. """

    feed_type = ExtendeRSSFeed
    title = "Typeidea Blog System"
    link = "/rss/"
    description = "typeidea is a blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_descirption(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html

