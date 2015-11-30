from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from ics import Calendar
from ics import Event as VEvent


from .serializers import EventSerializer, MeetingSerializer, HackerAgendaEventSerializer
from .models import Event, Meeting
from .forms import EventForm, MeetingForm


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


class MeetingAddView(CreateView):
    form_class = MeetingForm
    template_name = 'meeting_form.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        form.instance.event = event
        return super(MeetingAddView, self).form_valid(form)

    def get_success_url(self):
        return self.object.event.get_absolute_url()


class MeetingEditView(UpdateView):
    form_class = MeetingForm
    template_name = 'meeting_form.html'
    model = Meeting

    def get_success_url(self):
        return self.object.event.get_absolute_url()


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


def ical(request):
    events = Event.objects.filter(status__exact="r")
    cal = Calendar()
    for event in events:
        vevent = VEvent(
            name=event.title,
            begin=event.start,
            end=event.stop,
            description=event.description,
            location=event.place
        )
        cal.events.append(vevent)

    return HttpResponse(str(cal), content_type="text/calendar")


def interested(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.interested.add(request.user)
    return HttpResponseRedirect(event.get_absolute_url())


def not_interested(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.interested.remove(request.user)
    return HttpResponseRedirect(event.get_absolute_url())

def start_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if (event.status != 'r'):
        return HttpResponseForbidden("This event should be ready before being started")
    event.status = 'o'
    event.save()
    try:
        event.meeting.set_pad_contents(event.meeting.OJ)
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(event.get_absolute_url())

def stop_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if (event.status != 'o'):
        return HttpResponseForbidden("This event should be started before being stopped")
    event.status = 'f'
    event.save()
    try:
        event.meeting.PV = event.meeting.get_pad_contents()
        event.meeting.save()
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(event.get_absolute_url())

sm = short_url_maker("smartmonday")
linux = short_url_maker("install", "party")
git = short_url_maker("workshop", "git")
ag = short_url_maker("AG", "mandat")


from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('start', 'stop')
    filter_fields = ('place', 'start', 'stop', 'status', 'organizer', 'meeting')


class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()


class HackerAgendaAPI(APIView):
    def get(self, request, format=None):
        qs = Event.objects.filter(status="r").filter(start__isnull=False)
        events = HackerAgendaEventSerializer(qs, many=True)

        return Response({
            "org": "UrLab",
            "api": 0.1,
            "events": events.data
        })
