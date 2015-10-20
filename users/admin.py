from django.contrib import admin

from .models import User, MacAdress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    #list_display = ('balance',)
    list_filter = ('balance',)
    #search_fields = ('user',)


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder')
    # list_filter = ('adress',)
    search_fields = ('adress', 'holder')
