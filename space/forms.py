from django.forms import ModelForm

from .models import MacAdress


class MacAdressForm(ModelForm):
    class Meta:
        model = MacAdress
        fields = ['machine_name', 'adress']
