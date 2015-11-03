from django.contrib import admin
from .models import MacAdress


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder', 'machine_name')
    search_fields = ('adress', 'holder')
