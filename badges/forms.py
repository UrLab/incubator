import django.forms as forms
from badges.models import BadgeWear, Badge


class BadgeWearForm(forms.ModelForm):

    class Meta:
        model = BadgeWear
        fields = ('user', 'level')


class ApproveBadgeForm(forms.ModelForm):

    class Meta:
        model = Badge
        widgets = {'approved': forms.HiddenInput()}
        exclude = ['name', 'description', 'hidden', 'icon', 'proposed_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['approved'].value = True


class CreateBadgeForm(forms.ModelForm):

    class Meta:
        model = Badge
        widgets = {'approved': forms.HiddenInput()}
        exclude = ['proposed_by', 'approved']
