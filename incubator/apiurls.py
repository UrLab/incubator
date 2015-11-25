from rest_framework import routers

import events.views
import users.views
import projects.views
import stock.views
import space.views


api = routers.DefaultRouter()
api.register(r'events', events.views.EventViewSet)
api.register(r'meetings', events.views.MeetingViewSet)
api.register(r'users', users.views.UserViewSet)
api.register(r'projects', projects.views.ProjectViewSet)
api.register(r'stock/categories', stock.views.CategoryViewSet)
api.register(r'stock/products', stock.views.ProductViewSet)
api.register(r'space/openings', space.views.OpeningsViewSet)
api.register(r'space/pamela', space.views.PamelaViewSet, base_name="pamela")
