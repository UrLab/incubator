from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.wiki_home, name='wiki_home'),
]
