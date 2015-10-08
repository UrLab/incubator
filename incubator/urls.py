from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = patterns(
    '',
    url(r'^$', 'incubator.views.home', name='home'),
    url(r'^events/', include('events.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url('^register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url='/',

    ), name="register"),
)
