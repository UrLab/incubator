import django.forms as forms
from badges.models import BadgeWear, Badge


class BadgeWearForm(forms.ModelForm):
    """A form to give a user a badge"""
    class Meta:
        model = BadgeWear
        fields = ('user', 'level')


class ApproveBadgeForm(forms.ModelForm):
    """A form to approve a proposed badge"""
    class Meta:
        model = Badge
        widgets = {'approved': forms.HiddenInput()}
        exclude = ['name', 'description', 'hidden', 'icon', 'proposed_by']


class CreateBadgeForm(forms.ModelForm):
    """A form to create a new badge proposition"""

    class Meta:
        model = Badge
        widgets = {'approved': forms.HiddenInput()}
        exclude = ['proposed_by', 'approved']
