from django.urls import path
from django.contrib.auth.decorators import login_required
from users import views

urlpatterns = [
    path('profile', login_required(views.CurrentUserDetailView.as_view()), name='profile'),
    path('edit', login_required(views.UserEditView.as_view()), name='user_edit'),
    path('balance', login_required(views.balance), name='change_balance'),
    path('balance/spend', login_required(views.spend), name='balance_spend'),
    path('balance/product', login_required(views.buy_product), name='buy_product'),
    path('balance/top', login_required(views.top), name='balance_top'),
    path('balance/transfer', login_required(views.transfer), name='balance_transfer'),
    path('show_pamela', login_required(views.show_pamela), name='show_pamela'),
    path('hide_pamela', login_required(views.hide_pamela), name='hide_pamela'),
    path('<str:slug>', views.UserDetailView.as_view(), name='user_profile'),
    path('login/', views.login_view, name="login_view"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('debtmails/', views.send_debt_mail, name="debt_mail"),
    path('passwd/', login_required(views.change_passwd), name="chg_passwd"),
    path('admin/user/<int:id>/change_password', views.admin_change_passwd, name="admin_change_passwd"),
]
