from django.contrib import admin
from .models import MacAdress, SpaceStats


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder', 'machine_name')
    search_fields = ('adress', 'holder')


@admin.register(SpaceStats)
class SpaceStatsAdmin(admin.ModelAdmin):
    list_display = ('time', 'adress_count', 'user_count', 'unknown_mac_count')
    list_filter = ('time',)
