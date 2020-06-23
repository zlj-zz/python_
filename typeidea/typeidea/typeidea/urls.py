"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

AA2FA6A5C09CB2CC870E39D9AA751EFDC3B01159
口唇之欲
"""
import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views

# from blog.views import post_list, post_detail, PostDetailView
from config.views import LinkListView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import (IndexView, CategoryView, TagView, PostDetailView,
                        SearchView, AuthorView)
from blog.apis import PostViewSet, CategoryViewSet
from .autocomplete import CategoryAutocomplete, TagAutocomplete

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

urlpatterns = [
    # url(r'^api/post/', post_list, name='post-list'),
    # url(r'^api/post/', PostList.as_view(), name='post-list'),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/docs/', include_docs_urls(title='typeidea apis')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(),
        name='category-autocomplete'),
    url(r'^tag-autocomplete/$',
        TagAutocomplete.as_view(),
        name='tag-autocomplete'),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap,
        {'sitemaps': {
            'posts': PostSitemap
        }}),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$',
        CategoryView.as_view(),
        name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    # url(r'^post/(?P<post_id>\d+).html/$', post_detail, name='post-detail'),
    url(r'^post/(?P<post_id>\d+).html/$',
        PostDetailView.as_view(),
        name='post-detail'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^silk/', include('silk.urls', namespace='silk')),
    ]
