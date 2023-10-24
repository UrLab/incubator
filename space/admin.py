from django.contrib import admin
from .models import MacAdress, SpaceStatus, MusicOfTheDay, PrivateAPIKey


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder', 'machine_name')
    search_fields = ('adress', 'holder__username')


@admin.register(SpaceStatus)
class SpaceStatusAdmin(admin.ModelAdmin):
    list_display = ('time', 'is_open')
    list_filter = ('time', 'is_open')


@admin.register(MusicOfTheDay)
class MusicOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('url', 'irc_nick', 'day')
    list_filter = ('day', 'irc_nick')


@admin.register(PrivateAPIKey)
class PrivateAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'active', 'key')
    list_filter = ('user', 'active')
