from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import BadgeDetailView, promote_user,\
    BadgeHomeView, BadgeWearAddView

urlpatterns = [
    path('', BadgeHomeView.as_view(), name='badges_home_view'),
    path('add/<int:pk>/', BadgeWearAddView, name='badges_add'),
    path('add/', BadgeWearAddView, name='badges_add'),
    path(
        '<slug:action>/<str:username>/<int:pk>/', login_required(promote_user), name='promote_user'),
    path(
        '<int:pk>/', login_required(BadgeDetailView.as_view()), name='badge_view'),
]
