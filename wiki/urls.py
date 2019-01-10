from django.conf.urls import url

from .views import (wiki_home,)

urlpatterns = [
    url(r'^$', wiki_home, name='wiki_home'),
]
