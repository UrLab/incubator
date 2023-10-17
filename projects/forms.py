import re

from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Comment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['organizer']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 25}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        expr = re.compile(r"!\[.+\]\(http:\/\/.+\)")
        matches = expr.findall(content)

        if len(matches) > 0:
            self.add_error(
                "content",
                f"La description du projet contient des images en http non sécurisé ({' - '.join(matches)})"
            )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'project', 'author']
        widgets = {'project': forms.HiddenInput(), 'author': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        expr = re.compile(r"!\[.+\]\(http:\/\/.+\)")
        matches = expr.findall(content)

        if len(matches) > 0:
            self.add_error(
                "content",
                f"Le commentaire contient des images en http non sécurisé ({' - '.join(matches)})"
            )
