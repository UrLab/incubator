from django.conf.urls import patterns, include, url
from django.contrib import admin

import incubator.views
import incubator.apiurls
from incubator import settings
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern


urlpatterns = patterns(
    '',
    url(r'^$', 'incubator.views.home', name='home'),
    url(r'^spaceapi.json$', 'space.views.spaceapi', name="sapceapi"),
    url(r'^events/', include('events.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^accounts/', include('users.urls')),
    url(r'^space/', include('space.urls')),

    url(r'^sm', 'events.views.sm'),
    url(r'^linux', 'events.views.linux'),
    url(r'^git', 'events.views.git'),
    url(r'^ag', 'events.views.ag'),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^register/', incubator.views.RegisterView.as_view(), name="register"),

    url(r'^api/', include(incubator.apiurls.api.urls)),
    (r'^notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern()),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
