from django.conf.urls import patterns, url

from .views import pamela_list

urlpatterns = patterns(
    '',
    url(r'^pamela', pamela_list, name='pamela_list'),
)
