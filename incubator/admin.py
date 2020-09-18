from django.contrib import admin

from .models import ASBLYear


@admin.register(ASBLYear)
class ASBLYearAdmin(admin.ModelAdmin):
    list_display = ('start', 'stop')
