from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'balance', 'email', 'has_key', 'is_staff', 'is_member', 'created')
    list_filter = ('balance', 'has_key', 'is_staff', 'created')
    search_fields = ('username', 'email')
