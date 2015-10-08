from django.contrib import admin

from .models import Event, Meeting


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start', 'stop', 'place', 'organizer')
    list_filter = ('status', 'start', 'stop')
    search_fields = ('title', 'description', 'place')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'organizer')
    list_filter = ('start',)
    search_fields = ('OJ', 'PV', 'title')
