from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from users.decorators import no_troll_required
from .views import (
    EventDetailView, EventAddView, EventEditView, MeetingAddView, MeetingEditView,
    events_home, ical, not_interested, interested, import_pad, export_pad,
    add_point_to_next_meeting,
)

urlpatterns = patterns(
    '',
    url(r'^$', events_home, name='events_home'),
    url(r'^add$', no_troll_required(EventAddView.as_view()), name='add_event'),
    url(r'^urlab.ics$', ical, name='ical'),
    url(r'^edit/(?P<pk>[0-9]+)$', no_troll_required(EventEditView.as_view()), name='edit_event'),
    url(r'^import_pad/(?P<pk>[0-9]+)$', no_troll_required(import_pad), name='import_pad'),
    url(r'^export_pad/(?P<pk>[0-9]+)$', no_troll_required(export_pad), name='export_pad'),
    url(r'^(?P<pk>[0-9]+)', EventDetailView.as_view(), name='view_event'),
    url(r'^add_meeting/(?P<pk>[0-9]+)', no_troll_required(MeetingAddView.as_view()), name='add_meeting'),
    url(r'^edit_meeting/(?P<pk>[0-9]+)', no_troll_required(MeetingEditView.as_view()), name='edit_meeting'),
    url(r'^not_interested/(?P<pk>[0-9]+)$', login_required(not_interested), name='not_interested_event'),
    url(r'^interested/(?P<pk>[0-9]+)$', login_required(interested), name='interested_event'),

    # Private API
    url(r'^add_point_to_next_meeting', add_point_to_next_meeting, name='add_point_to_next_meeting'),
)
