from django.contrib import admin
from django.contrib import auth

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def not_a_troll(self, request, queryset):
        queryset.update(is_troll=False)
    not_a_troll.short_description = "Marquer comme NON-troll"

    def a_troll(self, request, queryset):
        queryset.update(is_troll=True)
    a_troll.short_description = "Marquer comme troll"

    actions = [not_a_troll, a_troll]

    list_display = ('username', 'balance', 'email', 'has_key', 'is_troll',
                    'is_staff', 'is_member', 'created')
    list_filter = ('balance', 'has_key', 'is_staff', 'created', 'is_troll')
    search_fields = ('username', 'email')

    add_form = auth.forms.UserCreationForm
    form = auth.forms.UserChangeForm
