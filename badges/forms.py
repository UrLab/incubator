from django.forms import ModelForm
from .models import BadgeWear


class BadgeWearForm(ModelForm):

    class Meta:
        model = BadgeWear
        fields = ('user', 'level')
