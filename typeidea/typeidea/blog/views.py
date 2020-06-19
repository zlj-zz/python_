from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Post, Tag, Category
from config.models import SideBar


class CommonViewMixin:
    """Docstring for CommonViewMixin. """
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())

        return context


class IndexView(CommonViewMixin, ListView):
    """Docstring for PostListView. """

    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """Docstring for CategoryView. """
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        # `get_object_or_404`: get object , if not exists return 404
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })

        return context

    def get_queryset(self):

        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')

        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    """Docstring for TagView. """
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })

        return context

    def get_queryset(self):

        queryset = super().get_queryset()
        tag = self.kwargs.get('tag_id')

        return queryset.filter(tag=tag)


class PostDetailView(CommonViewMixin, DetailView):
    """Docstring for PostDetailView. """

    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    comtext_object_name = 'post'
    pk_url_kwarg = 'post_id'


class SearchView(IndexView):
    """Docstring for SearchView. """
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', ''),
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    """Docstring for AuthorView. """
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.GET.get('owner_id')

        return queryset.filter(owner_id=author_id)


'''
def post_list(request, category_id=None, tag_id=None):
    """TODO: Docstring for post_list.

    :request: TODO
    :returns: TODO

    """

    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    """TODO: Docstring for post_detail.

    :request: TODO
    :post_id: TODO
    :returns: TODO

    """

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoseNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())

    return render(request, 'blog/detail.html', context=context)
'''
