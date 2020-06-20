# -*- coding:UTF-8 -*-
"""tag: comment_block

File Name: comment_block.py
Last Modified: 
Created Time: 2020-06-20

<++>
"""

__author__ = 'zachary'

from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    """TODO: Docstring for comment_block.

    :target: TODO
    :returns: TODO

    """

    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target)
    }
