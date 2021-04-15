from django.urls import path

from django.views.generic import TemplateView
from .views import conference_list

urlpatterns = [
    path('', TemplateView.as_view(template_name='streams/stream-http.html'),
         name='stream-main'),
    path('conferences/', conference_list ),
]
