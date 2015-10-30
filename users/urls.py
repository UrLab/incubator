from django.conf.urls import patterns, url

from .views import CurrentUserDetailView, change_balance

urlpatterns = patterns(
    '',
    url(r'^profile', CurrentUserDetailView.as_view(), name='profile'),
    url(r'^balance', change_balance, name='change_balance'),
)
