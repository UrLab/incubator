from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from django import forms
from .models import User
from stock.models import Product


class UserDescriptionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["description", ]


class TolerantDecimalField(forms.DecimalField):
    def clean(self, value):
        value = value.replace(',', '.')
        return super(TolerantDecimalField, self).clean(value)


class BalanceForm(forms.Form):
    value = TolerantDecimalField(
        label="Montant",
        max_digits=6,
        decimal_places=2,
        min_value=0,
        max_value=500
    )


class TopForm(BalanceForm):
    location = forms.ChoiceField(
        choices=[
            ('BANK', "Virement"),
            ('CASH', "Caisse"),
        ],
        widget=forms.RadioSelect,
    )


class SpendForm(BalanceForm):
    name = forms.CharField(
        max_length=100,
        label="Nom du produit",
    )


class ProductBuyForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())


class TransferForm(BalanceForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.order_by('username'),
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'newsletter', 'description']


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification.")
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def auth_user(self):
        user = authenticate(
            username=self.cleaned_data.get("username"),
            password=self.cleaned_data.get("password1"),
        )

        return user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_("Old Password"),
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_("New Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification.")
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("new_password2")

        if password != confirm_password:
            self.add_error('new_password', "Les mots de passe ne sont pas identiques!")


class AdminChangePasswordForm(forms.Form):

    new_password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_("New Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification.")
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("new_password2")

        if password != confirm_password:
            self.add_error('new_password', "Les mots de passe ne sont pas identiques!")
