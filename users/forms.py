from django.forms import ModelForm

from .models import User


class BalanceForm(ModelForm):
    class Meta:
        model = User
        fields = ['balance']
