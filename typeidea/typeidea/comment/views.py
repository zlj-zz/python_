from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    """Docstring for CommentView. """

    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        """TODO: Docstring for post.

        :request: TODO
        :*args: TODO
        :**kwargs: TODO
        :returns: TODO

        """

        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'succed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)
