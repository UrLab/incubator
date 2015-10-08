from django.contrib import admin

from .models import Hacker, MacAdress


@admin.register(Hacker)
class HackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    # list_filter = ('balance',)
    search_fields = ('user',)


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder')
    # list_filter = ('adress',)
    search_fields = ('adress', 'holder')
