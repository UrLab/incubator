from django import forms

from .models import User


class BalanceForm(forms.Form):
    value = forms.DecimalField(max_digits=6, decimal_places=2)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
