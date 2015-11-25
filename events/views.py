from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q


from .serializers import EventSerializer, MeetingSerializer
from .models import Event, Meeting
from .forms import EventForm


class EventAddView(CreateView):
    form_class = EventForm
    template_name = 'add_event.html'

    def get_initial(self):
        return {
            'organizer': self.request.user,
        }


class EventEditView(UpdateView):
    form_class = EventForm
    model = Event
    template_name = 'add_event.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


def events_home(request):
    futureQ = Q(stop__gt=timezone.now())
    readyQ = Q(status__exact="r")

    base = Event.objects.select_related('meeting')

    context = {
        'future': base.filter(futureQ & readyQ).order_by('start'),
        'past': base.filter(~futureQ & readyQ).order_by('-start')[:10],
        'incubation': base.filter(~readyQ),
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


def import_pad(request, pk):
    event = get_object_or_404(Event, pk=pk)
    meeting = event.meeting
    if meeting.PV:
        return HttpResponseForbidden("This meeting already has a PV")

    meeting.PV = meeting.get_pad_contents()
    meeting.save()

    return HttpResponseRedirect(event.get_absolute_url())


sm = short_url_maker("smartmonday")
linux = short_url_maker("install", "party")
git = short_url_maker("workshop", "git")
ag = short_url_maker("AG", "mandat")


from rest_framework import filters
from rest_framework import viewsets


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('start', 'stop')
    filter_fields = ('place', 'start', 'stop', 'status', 'organizer', 'meeting')


class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()
