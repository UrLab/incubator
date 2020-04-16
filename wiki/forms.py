from django.forms import ModelForm, Textarea

from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['creator', 'last_modified']

        widgets = {
            'content': Textarea(attrs={'rows': 20}),
            'commit': Textarea(attrs={'rows': 3}),
        }
