from django.conf.urls import patterns, url

from .views import EventDetailView

urlpatterns = patterns(
    '',
    url(r'^$', 'events.views.events_home', name='events_home'),
    url(r'^add$', 'events.views.add_event', name='add_event'),
    url(r'^(?P<pk>[0-9]+)', EventDetailView.as_view(), name='view_event')
)
