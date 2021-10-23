from django.urls import path
from django.contrib.auth.decorators import login_required
import badges.views as bviews

urlpatterns = [
    path('', bviews.BadgeHomeView.as_view(), name='badges_home_view'),
    path('add/<int:pk>/', bviews.BadgeWearAddView, name='badges_add'),
    path('propose/', login_required(bviews.ProposeBadgeView.as_view()), name='badge_proposal'),
    path('<int:pk>/', login_required(bviews.BadgeDetailView.as_view()), name='badge_view'),
    path('<int:pk>/review', login_required(bviews.BadgeApproveView.as_view()), name='badge_review'),
    path('<slug:action>/<str:username>/<int:pk>/', login_required(bviews.promote_user), name='promote_user'),
]
