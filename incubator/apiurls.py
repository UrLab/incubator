from django.conf.urls import include, url
from rest_framework import routers

import events.views
import users.views
import projects.views
import stock.views
import space.views
import streams.api_views


api = routers.DefaultRouter()
api.register('events', events.views.EventViewSet)
api.register('meetings', events.views.MeetingViewSet)
api.register('users', users.views.UserViewSet)
api.register('projects', projects.views.ProjectViewSet)
api.register('stock/categories', stock.views.CategoryViewSet)
api.register('stock/products', stock.views.ProductViewSet)
api.register('streams/urtip', streams.api_views.UrtipViewSet)
api.register('space/openings', space.views.OpeningsViewSet)
api.register('space/pamela', space.views.PamelaViewSet, basename="pamela")
api.register('space/motd', space.views.MotdViewSet)


urlpatterns = [
    url('^hackeragenda', events.views.HackerAgendaAPI.as_view()),
    url('^events/next_meeting', events.views.NextMeetingAPI.as_view()),
    url('^', include(api.urls)),
]
