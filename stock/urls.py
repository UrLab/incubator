from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import payment_transaction_home


urlpatterns = [
    path("transactions", login_required(payment_transaction_home), name="transactions"),
]
