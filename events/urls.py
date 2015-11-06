from django.conf.urls import patterns, url

from .views import EventDetailView, EventAddView, EventEditView

urlpatterns = patterns(
    '',
    url(r'^$', 'events.views.events_home', name='events_home'),
    url(r'^add$', EventAddView.as_view(), name='add_event'),
    url(r'^edit/(?P<pk>[0-9]+)$', EventEditView.as_view(), name='edit_event'),
    url(r'^(?P<pk>[0-9]+)', EventDetailView.as_view(), name='view_event')
)
