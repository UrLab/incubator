from django.contrib import admin

from .models import ASBLYear
from users.models import Membership


class UserInline(admin.TabularInline):
    model = Membership
    extra = 1


@admin.register(ASBLYear)
class ASBLYearAdmin(admin.ModelAdmin):
    list_display = ('start', 'stop')

    inlines = (UserInline, )
