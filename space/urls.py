from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import pamela_list, status_change, DeleteMACView, motd_change

urlpatterns = patterns(
    '',
    url(r'^pamela', pamela_list, name='pamela_list'),
    url(r'^change_status', status_change, name='change_status'),
    url(r'^change_motd', motd_change, name='change_motd'),
    url(r'^remove_mac/(?P<pk>[0-9]+)', login_required(DeleteMACView.as_view()), name="delete_mac"),
)
