from django import forms
from .models import Project, Comment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['organizer']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 25}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'project', 'author']
        widgets = {'project': forms.HiddenInput(), 'author': forms.HiddenInput()}
