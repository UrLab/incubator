from django.urls import include, path
from django.contrib import admin

import incubator.views
import incubator.apiurls
from incubator import settings
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

import redir.views
import events.views
import incubator.views
import space.views

urlpatterns = [
    path('', incubator.views.home, name='home'),
    path('spaceapi.json', space.views.spaceapi, name="spaceapi"),
    path('events/', include('events.urls')),
    path('projects/', include('projects.urls')),
    path('accounts/', include('users.urls')),
    path('space/', include('space.urls')),

    path('sm', events.views.sm),
    path('linux', events.views.linux),
    path('git', events.views.git),
    path('ag', events.views.ag),

    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', incubator.views.RegisterView.as_view(), name="register"),

    path('api/', include('incubator.apiurls')),
    path('notifications/', get_nyt_pattern()),
    path('wiki/', get_wiki_pattern()),
    path('r/<slug:short_name>', redir.views.short_url, name='redirection'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = incubator.views.error_view(400, "Impossible de traiter cette requête")
handler403 = incubator.views.error_view(403, "Tu n'as pas la permission de faire ça")
handler404 = incubator.views.error_view(404, "Impossible de trouver ça")
handler500 = incubator.views.error_view(500, "Une erreur serveur s'est produite")
