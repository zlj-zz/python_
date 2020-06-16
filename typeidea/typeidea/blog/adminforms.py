from django import forms


class PostAdminForm(forms.ModelForm):
    """Docstring for PostAdminForm. """

    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
