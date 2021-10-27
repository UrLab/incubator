from django.contrib import admin

from .models import Badge, BadgeWear


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(BadgeWear)
class BadgeWearAdmin(admin.ModelAdmin):

    @staticmethod
    def badge_level(obj):
        if obj.badge.has_level:
            return obj.get_level_display()
        return "-"

    list_display = ('badge', 'user', 'badge_level', 'timestamp', 'attributor')
