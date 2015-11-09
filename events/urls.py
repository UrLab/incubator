from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import EventDetailView, EventAddView, EventEditView, events_home

urlpatterns = patterns(
    '',
    url(r'^$', events_home, name='events_home'),
    url(r'^add$', login_required(EventAddView.as_view()), name='add_event'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(EventEditView.as_view()), name='edit_event'),
    url(r'^(?P<pk>[0-9]+)', EventDetailView.as_view(), name='view_event')
)
