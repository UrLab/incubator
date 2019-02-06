from django.forms import ModelForm, Textarea

from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['creator', 'nbr_revision']

        widgets = {
            'content': Textarea(attrs={'rows': 25}),
        }
