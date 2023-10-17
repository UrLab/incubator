import re

from django.forms import ModelForm, Textarea

from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['creator', 'last_modifier']

        widgets = {
            'content': Textarea(attrs={'rows': 20}),
            'commit': Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        expr = re.compile(r"!\[.+\]\(http:\/\/.+\)")
        matches = expr.findall(content)

        if len(matches) > 0:
            self.add_error(
                "content",
                f"L'article contient des images en http non sécurisé ({' - '.join(matches)})"
            )
