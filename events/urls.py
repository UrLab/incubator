from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    EventDetailView, EventAddView, EventEditView, MeetingAddView,
    MeetingEditView, events_home, ical, not_interested, interested, import_pad,
    export_pad, add_point_to_next_meeting,
)

urlpatterns = [
    path('', events_home, name='events_home'),
    path('add', EventAddView.as_view(), name='add_event'),
    path('urlab.ics', ical, name='ical'),
    path('edit/<int:pk>', EventEditView.as_view(), name='edit_event'),
    path('import_pad/<int:pk>', import_pad, name='import_pad'),
    path('export_pad/<int:pk>', export_pad, name='export_pad'),
    path('<int:pk>', EventDetailView.as_view(), name='view_event'),
    path('add_meeting/<int:pk>', MeetingAddView.as_view(), name='add_meeting'),
    path('edit_meeting/<int:pk>', MeetingEditView.as_view(), name='edit_meeting'),
    path('not_interested/<int:pk>', login_required(not_interested), name='not_interested_event'),
    path('interested/<int:pk>', login_required(interested), name='interested_event'),

    # Private API
    path('add_point_to_next_meeting', add_point_to_next_meeting, name='add_point_to_next_meeting'),
]
