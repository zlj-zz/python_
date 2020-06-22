# -*- coding:UTF-8 -*-
"""autocomplete interface

File Name: autocomplete.py
Last Modified: 
Created Time: 2020-06-22


"""

__author__ = 'zachary'

from dal import autocomplete
from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    """Docstring for CategoryAutocomplete. """
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    """Docstring for TagAutocomplete. """
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = Tag.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
