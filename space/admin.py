from django.contrib import admin
from .models import MacAdress


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder')
    list_filter = ('hidden',)
    search_fields = ('adress', 'holder')
