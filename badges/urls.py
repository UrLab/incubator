from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import BadgeDetailView, promote_user,\
    BadgeHomeView, BadgeWearAddView

urlpatterns = [
    url(r'^$', BadgeHomeView.as_view(), name='badges_home_view'),
    url(r'^add/(?P<pk>[\w-]+)/$', BadgeWearAddView, name='badges_add'),

    url(r'^add/$', BadgeWearAddView, name='badges_add'),

    url(r'^(?P<action>[\w-]+)/(?P<username>[\w-]+)/(?P<pk>[\w-]+)/{0,}$',
        login_required(promote_user), name='promote_user'),

    url(r'^(?P<pk>[\w-]+)/{0,}$',
        login_required(BadgeDetailView.as_view()), name='badge_view'),
]
