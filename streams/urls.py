from django.urls import path

from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='streams/stream-http.html'),
         name='stream-main'),
]
