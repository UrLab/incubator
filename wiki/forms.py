from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['creator', 'last_modifier']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 20}),
            'commit': forms.Textarea(attrs={'rows': 3}),
        }


class DiffForm(forms.Form):
    base_commit = forms.ModelChoiceField(queryset=Article.history.model.objects.all(), required=True, label="Version de base")
    comp_commit = forms.ModelChoiceField(queryset=Article.history.model.objects.all(), required=True, label="Version à comparer")

    # def __init__(self, *args, **kwargs):
    #     if 'article' in kwargs:
    #         article = kwargs.pop('article')
