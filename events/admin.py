from django.contrib import admin

from .models import Event, Meeting


class MeetingInline(admin.StackedInline):
    model = Meeting
    filter_horizontal = ('members',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start', 'stop', 'place', 'organizer')
    list_filter = ('status', 'start', 'stop')
    search_fields = ('title', 'description', 'place')

    filter_horizontal = ('interested',)
    inlines = (MeetingInline,)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('event',)
    search_fields = ('OJ', 'PV')
    filter_horizontal = ('members',)
