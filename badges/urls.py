from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import BadgeDetailView, promote_user

urlpatterns = [
    url(r'^(?P<action>[\w-]+)/(?P<username>[\w-]+)/(?P<pk>[\w-]+)/{0,}$',
        login_required(promote_user), name='promote_user'),

    url(r'^(?P<pk>[\w-]+)/{0,}$',
        login_required(BadgeDetailView.as_view()), name='badge_view'),
]
