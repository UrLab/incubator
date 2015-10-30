from django.forms import ModelForm
from django import forms

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['organizer']
