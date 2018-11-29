from django.forms import ModelForm, Textarea

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['organizer','likes']

        widgets = {
            'content': Textarea(attrs={'rows': 25}),
        }
