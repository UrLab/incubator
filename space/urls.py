from django.conf.urls import patterns, url

from .views import pamela_list, status_change

urlpatterns = patterns(
    '',
    url(r'^pamela', pamela_list, name='pamela_list'),
    url(r'^change_status', status_change, name='change_status'),
)
