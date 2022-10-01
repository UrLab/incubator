import django.forms as forms
from badges.models import BadgeWear, Badge


class LeveledBadgeWearForm(forms.ModelForm):
    """A form to give a user a badge with a level"""
    class Meta:
        model = BadgeWear
        fields = ('user', 'level')


class BadgeWearForm(forms.ModelForm):
    """A form to give a user a badge"""
    class Meta:
        model = BadgeWear
        fields = ('user', )


class ApproveBadgeForm(forms.ModelForm):
    """A form to approve a proposed badge"""
    class Meta:
        model = Badge
        widgets = {'approved': forms.HiddenInput()}
        exclude = ['name', 'description', 'hidden', 'icon', 'proposed_by', 'has_level']


class CreateBadgeForm(forms.ModelForm):
    """A form to create a new badge proposition"""
    anonymous = forms.BooleanField(label="Proposer anonymement", required=False)

    class Meta:
        model = Badge
        widgets = {
            'approved': forms.HiddenInput(),
            'proposed_by': forms.HiddenInput()
        }
        exclude = ['approved']

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['anonymous']:
            cleaned_data['proposed_by'] = None
        return cleaned_data
