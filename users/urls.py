from django.conf.urls import patterns, url

from .views import CurrentUserDetailView, balance, UserDetailView, UserEditView

urlpatterns = patterns(
    '',
    url(r'^profile', CurrentUserDetailView.as_view(), name='profile'),
    url(r'^edit', UserEditView.as_view(), name='user_edit'),
    url(r'^balance', balance, name='change_balance'),
    url(r'^(?P<slug>.+)', UserDetailView.as_view(), name='user_profile'),
)
