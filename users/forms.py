from django.forms import ModelForm

from .models import User


class BalanceForm(ModelForm):
    class Meta:
        model = User
        fields = ['balance']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
