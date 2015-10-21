from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from django.views.generic.detail import DetailView

from .serializers import EventSerializer
from datetimewidget.widgets import DateTimeWidget

from .models import Event
from .forms import EventForm

from django.utils import timezone


def events_home(request):
    context = {
        'future': Event.objects.filter(stop__gt=timezone.now()).order_by('start')[:10],
        'past': Event.objects.exclude(stop__gt=timezone.now()).order_by('-start')[:10],
    }

    return render(request, "events_home.html", context)


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            return HttpResponseRedirect(reverse('view_event', args=[event.id]))

    else:
        form = EventForm()

    form.fields['start'].widget = DateTimeWidget(
        attrs=form.fields['start'].widget.attrs,
        usel10n=True,
        bootstrap_version=3
    )
    form.fields['stop'].widget = DateTimeWidget(
        attrs=form.fields['stop'].widget.attrs,
        usel10n=True,
        bootstrap_version=3
    )

    return render(request, 'add_event.html', {'form': form})


class EventDetailView(DetailView):

    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
