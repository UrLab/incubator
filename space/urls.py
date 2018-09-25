from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import (pamela_list, status_change, DeleteMACView, motd_change,
                    openings_data, full_pamela, get_user_mac, get_mac_user)


urlpatterns = [
    url(r'^pamela$', pamela_list, name='pamela_list'),
    url(r'^change_status$', status_change, name='change_status'),
    url(r'^change_motd$', motd_change, name='change_motd'),
    url(r'^remove_mac/(?P<pk>[0-9]+)$', login_required(DeleteMACView.as_view()), name="delete_mac"),
    url(r'^openings_data$', openings_data, name='openings_graph_data'),

    url(r'^private_pamela.json$', full_pamela, name='private_pamela'),
    url(r'^user_mac.json$', get_user_mac, name='user_mac'),
    url(r'^mac_user.json$', get_mac_user, name='mac_user'),

]
