from django.shortcuts import render
from .models import Event
from .forms import EventForm

from datetime import datetime


def events_home(request):
    context = {
        'future': Event.objects.filter(stop__gt=datetime.now()).order_by('start')[:10],
        'past': Event.objects.exclude(stop__gt=datetime.now()).order_by('-start')[:10],
    }

    return render(request, "events_home.html", context)


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})
