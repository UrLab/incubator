from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    balance, UserDetailView, CurrentUserDetailView,
    UserEditView, spend, top, transfer, show_pamela, hide_pamela, buy_product,
    login_view)

urlpatterns = [
    path('profile', login_required(CurrentUserDetailView.as_view()), name='profile'),
    path('edit', login_required(UserEditView.as_view()), name='user_edit'),
    path('balance', login_required(balance), name='change_balance'),
    path('balance/spend', login_required(spend), name='balance_spend'),
    path('balance/product', login_required(buy_product), name='buy_product'),
    path('balance/top', login_required(top), name='balance_top'),
    path('balance/transfer', login_required(transfer), name='balance_transfer'),
    path('show_pamela', login_required(show_pamela), name='show_pamela'),
    path('hide_pamela', login_required(hide_pamela), name='hide_pamela'),
    path('<slug:slug>', UserDetailView.as_view(), name='user_profile'),
    path('login/', login_view, name="login_view"),
]
