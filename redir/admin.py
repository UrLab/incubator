from django.contrib import admin
from .models import Redirection


class RedirectionAdmin(admin.ModelAdmin):
    '''
        Admin View for Redirection
    '''
    list_display = ('name', 'target')
    search_fields = ('name', 'target')


admin.site.register(Redirection, RedirectionAdmin)
