from events.models import Conference
from django.shortcuts import render


def conference_list(request):
    conferences = Conference.objects.all()
    return render(request, "streams/conferences.html", {"conferences": conferences})
