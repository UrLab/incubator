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
    url(r'^spaceapi.json$', 'space.views.spaceapi', name="spaceapi"),
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

    url(r'^api/', include('incubator.apiurls')),
    (r'^notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern()),
    url(r'^r/(?P<short_name>.+)', 'redir.views.short_url', name='redirection'),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = incubator.views.error_view(400, "Impossible de traiter cette requête")
handler403 = incubator.views.error_view(403, "Tu n'as pas la permission de faire ça")
handler404 = incubator.views.error_view(404, "Impossible de trouver ça")
handler500 = incubator.views.error_view(500, "Une erreur serveur s'est produite")
