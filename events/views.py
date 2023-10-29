from datetime import timedelta

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
# from datetime import datetime
from actstream import action
from ics import Calendar
from ics import Event as VEvent
from users.decorators import permission_required
from users.mixins import PermissionRequiredMixin
from incubator.settings import EVENTS_PER_PAGE

from space.decorators import private_api
from realtime.helpers import send_message

from .serializers import EventSerializer, MeetingSerializer, HackerAgendaEventSerializer, FullMeetingSerializer
from .models import Event, Meeting
from .forms import EventForm, MeetingForm

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from constance import config as dyn_config


class EventAddView(PermissionRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'add_event.html'
    permission_required = 'events.add_event'

    def get_initial(self):
        return {
            'organizer': self.request.user,
        }

    def form_valid(self, form):
        ret = super(EventAddView, self).form_valid(form)
        action.send(self.request.user, verb='a créé', action_object=self.object)

        return ret


class EventEditView(PermissionRequiredMixin, UpdateView):
    form_class = EventForm
    model = Event
    template_name = 'add_event.html'
    permission_required = 'events.change_event'

    def form_valid(self, form):
        ret = super(EventEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


def talks(request):
    cutoff = timezone.now()
    events = Event.objects.filter(is_talk=True)
    future_events = events.filter(start__gt=cutoff)
    past_events = events.filter(stop__lt=cutoff)
    return render(
        request, 'talks.html',
        {
            'live': events.filter(start__lt=cutoff + timedelta(minutes=30), stop__gt=cutoff - timedelta(hours=2)).first(),
            'future_events': future_events,
            'past_events': past_events,
            'stream_url': dyn_config.LIVESTREAM_URL,
        }
    )


class MeetingAddView(PermissionRequiredMixin, CreateView):
    form_class = MeetingForm
    template_name = 'meeting_form.html'
    permission_required = 'events.add_meeting'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        form.instance.event = event
        return super(MeetingAddView, self).form_valid(form)

    def get_success_url(self):
        return self.object.event.get_absolute_url()


class MeetingEditView(PermissionRequiredMixin, UpdateView):
    form_class = MeetingForm
    template_name = 'meeting_form.html'
    model = Meeting
    permission_required = 'events.change_meeting'

    def get_success_url(self):
        return self.object.event.get_absolute_url()


def events_home(request):
    futureQ = Q(stop__gt=timezone.now())  # NOQA
    readyQ = Q(status__exact="r")  # NOQA

    # Par défaut on envoie la page 0 des evenement futurs
    offset = request.GET.get("offset", 0)
    type = request.GET.get("type", "future")
    try:
        offset = int(offset) if offset is not None else 0
    except ValueError:
        return HttpResponseBadRequest(
            "La valeur de l'offset n'est pas correcte")

    type = type if type is not None else "future"

    base = Event.objects.select_related('meeting')
    search_term = request.GET.get('search_term', None)
    if search_term:
        base = base.filter(title__contains=search_term)
    isLastPage = False

    if type == "future":
        events = base.filter(futureQ & readyQ).order_by('start')
    elif type == "past":
        events = base.filter(~futureQ & readyQ).order_by('-start')
    elif type == "incubation":
        events = base.filter(~readyQ).order_by('-id')
    else:
        return HttpResponseBadRequest("Le type d'évenement n'est pas correct")

    nbPages = events.count() // EVENTS_PER_PAGE

    if offset > nbPages or offset < 0:
        return HttpResponseBadRequest("La valeur de l'offset doit être \
            comprise entre 0 et {}".format(nbPages))

    if (offset + 1) * EVENTS_PER_PAGE < events.count():
        context = events[  # Takes a slice of the event array
            offset * EVENTS_PER_PAGE:(offset + 1) * EVENTS_PER_PAGE]
    else:
        context = events[offset * EVENTS_PER_PAGE:]
        isLastPage = True  # Pour pouvoir dire qu'il n'y a pas plus de page

    vars = {
        'events': context,
        'last': isLastPage,
        'type': type,
        'offset': offset + 1,
        'nbPage': nbPages,
        'range': range(1, nbPages + 2),
        'search_term': search_term if search_term else ''}
    return render(request, "events_home.html", vars)


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


def ical(request):
    events = Event.objects.filter(status__exact="r")
    cal = Calendar()
    for event in events:
        vevent = VEvent(
            name=event.title,
            begin=event.start,
            end=event.stop,
            description=event.get_absolute_full_url(),
            location=event.place
        )
        cal.events.add(vevent)

    return HttpResponse(str(cal), content_type="text/calendar")


def interested(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.interested.add(request.user)
    return HttpResponseRedirect(event.get_absolute_url())


def not_interested(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.interested.remove(request.user)
    return HttpResponseRedirect(event.get_absolute_url())


@permission_required('events.run_meeting')
def export_pad(request, pk):
    event = get_object_or_404(Event, pk=pk)
    meeting = event.meeting
    if not meeting:
        return HttpResponseForbidden("This is not a meeting")
    if not meeting.OJ:
        return HttpResponseForbidden("This meeting has no OJ")
    if meeting.PV:
        return HttpResponseForbidden("This meeting is already finished")
    if meeting.ongoing:
        return HttpResponseForbidden("This meeting is already ongoing")

    meeting.set_pad_contents(meeting.OJ)
    send_message(key="meeting.start",
                 message="On lance la réunion ! Pad: {url}",
                 url=meeting.pad)
    meeting.ongoing = True
    meeting.save()
    return HttpResponseRedirect(event.get_absolute_url())


@permission_required('events.run_meeting')
def import_pad(request, pk):
    event = get_object_or_404(Event, pk=pk)
    meeting = event.meeting
    if not meeting:
        return HttpResponseForbidden("This is not a meeting")

    meeting.PV = meeting.get_pad_contents()
    action.send(request.user, verb='a cloturé', action_object=event)
    meeting.save()
    return HttpResponseRedirect(event.get_absolute_url())


sm = short_url_maker("smartmonday")
linux = short_url_maker("install", "party")
git = short_url_maker("workshop", "git")
ag = short_url_maker("AG", "mandat")


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('start', 'stop')
    filter_fields = ('place', 'start', 'stop', 'status', 'organizer', 'meeting')


class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()


def get_next_meeting():
    return (
        Meeting.objects
        .filter(
            event__start__gte=timezone.now(),
            ongoing=False
        )
        .order_by('event__start')
        .first()
    )


@private_api(point=str)
def add_point_to_next_meeting(request, point):
    meeting = get_next_meeting()
    if meeting is None:
        return JsonResponse(
            {
                "error": "There is no future meeting",
                "hint": "Create a new event with an OJ",
            },
            status=404)
    meeting.OJ += '\n* ' + point
    meeting.save()
    r = {'new_point': point, 'full_oj': meeting.OJ}
    return JsonResponse(r, safe=False)


def attending(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.meeting.members.add(request.user)
    return HttpResponseRedirect(event.get_absolute_url())


def not_attending(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.meeting.members.remove(request.user)
    return HttpResponseRedirect(event.get_absolute_url())


class NextMeetingAPI(APIView):
    def get(self, request, format=None):
        data = FullMeetingSerializer(get_next_meeting(), context={'request': request}).data
        return Response(data)


class HackerAgendaAPI(APIView):
    def get(self, request, format=None):
        qs = Event.objects.filter(status="r").filter(start__isnull=False)
        events = HackerAgendaEventSerializer(qs, many=True)

        return Response({
            "org": "UrLab",
            "api": 0.1,
            "events": events.data
        })
