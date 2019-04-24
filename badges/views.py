from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView

from .models import Badge, BadgeWear
# Create your views here.


class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badge_detail.html'
    context_object_name = 'badge'


class BadgeWearAddView(CreateView):
    form_class = BadgeWear
    template_name = 'add_badgewear.html'

    def get_initial(self):
        return {
            'attributor': self.request.user,
        }
