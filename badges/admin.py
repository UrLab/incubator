from django.contrib import admin

from .models import Badge, BadgeWear

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(BadgeWear)
class BadgeWearAdmin(admin.ModelAdmin):
    list_display = ('badge', 'user', 'level', 'action_counter', 'timestamp', 'attributor')
