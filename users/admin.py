from django.contrib import admin
from django.contrib import auth

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'balance', 'email', 'has_key', 'is_superuser',
                    'is_member', 'created')
    list_filter = ('balance', 'has_key', 'is_superuser', 'created')
    search_fields = ('username', 'email')

    add_form = auth.forms.UserCreationForm
    form = auth.forms.UserChangeForm
