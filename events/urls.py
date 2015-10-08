from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'events.views.events_home', name='events_home'),
    url(r'^add$', 'events.views.add_event', name='add_event'),
)
