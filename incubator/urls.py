from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


import events.views
import users.views
import projects.views


router = routers.DefaultRouter()
router.register(r'events', events.views.EventViewSet)
router.register(r'users', users.views.UserViewSet)
router.register(r'projects', projects.views.ProjectViewSet)


urlpatterns = patterns(
    '',
    url(r'^$', 'incubator.views.home', name='home'),
    url(r'^events/', include('events.urls')),
    url(r'^projects/', include('projects.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url='/',

    ), name="register"),

    url(r'^api/', include(router.urls)),
)
