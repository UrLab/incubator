from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import CurrentUserDetailView, balance, UserDetailView, UserEditView, spend, top, transfer, show_pamela, hide_pamela

urlpatterns = patterns(
    '',
    url(r'^profile', login_required(CurrentUserDetailView.as_view()), name='profile'),
    url(r'^edit', login_required(UserEditView.as_view()), name='user_edit'),
    url(r'^balance$', login_required(balance), name='change_balance'),
    url(r'^balance/spend', login_required(spend), name='balance_spend'),
    url(r'^balance/top', login_required(top), name='balance_top'),
    url(r'^balance/transfer', login_required(transfer), name='balance_transfer'),
    url(r'^show_pamela', login_required(show_pamela), name='show_pamela'),
    url(r'^hide_pamela', login_required(hide_pamela), name='hide_pamela'),
    url(r'^(?P<slug>.+)', UserDetailView.as_view(), name='user_profile'),
)
