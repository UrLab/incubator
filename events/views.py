from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.utils import timezone
from rest_framework import viewsets


from .serializers import EventSerializer
from .models import Event
from .forms import EventForm


class EventAddView(CreateView):
    form_class = EventForm
    template_name = 'add_event.html'


class EventEditView(UpdateView):
    form_class = EventForm
    model = Event
    template_name = 'add_event.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


def events_home(request):
    context = {
        'future': Event.objects.filter(stop__gt=timezone.now()).order_by('start')[:10],
        'past': Event.objects.exclude(stop__gt=timezone.now()).order_by('-start')[:10],
    }

    return render(request, "events_home.html", context)


def short_url_maker(*keywords):
    def filter_func(request):
        events = Event.objects.exclude(stop__lt=timezone.now()).order_by('start')
        for kw in keywords:
            events = events.filter(title__icontains=kw)

        if len(events) == 0:
            return HttpResponseRedirect(reverse('events_home'))
        else:
            return HttpResponseRedirect(events[0].get_absolute_url())

    return filter_func


sm = short_url_maker("smartmonday")
linux = short_url_maker("install", "party")
git = short_url_maker("workshop", "git")
ag = short_url_maker("AG", "mandat")


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
