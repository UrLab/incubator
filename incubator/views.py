# from datetime import datetime
from django.utils import timezone
from django.views.generic.edit import CreateView
from users.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from actstream.models import Action

from space.djredis import get_redis, space_is_open
from events.models import Event
from realtime.helpers import feed_reducer

from constance import config as dyn_config


def error_view(code, msg=""):
    def view(request, excpetion=""):
        response = render(request, "error.html", {'code': code, 'message': msg})
        response.status_code = code
        return response
    return view


def home(request):
    client = get_redis()
    stream = []
    if request.user.is_authenticated:
        STREAM_SIZE = 20  # NOQA
        stream = Action.objects.filter(public=True).prefetch_related('target', 'actor', 'action_object')[:STREAM_SIZE * 2]
        stream = feed_reducer(stream)[:STREAM_SIZE]

    return render(request, "home.html", {
        "space_open": space_is_open(client),
        "message": dyn_config.HOMEPAGE_MESSAGE,
        "message_type": dyn_config.HOMEPAGE_MESSAGE_TYPE,
        "events": Event.objects.filter(stop__gt=timezone.now(), status__exact="r"),
        "stream": stream,
        "event_page": False,
    })


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def get_initial(self):
        initial = super(RegisterView, self).get_initial()
        initial = initial.copy()
        initial['username'] = self.request.GET.get("username")
        return initial

    def form_valid(self, form):
        ret = super(RegisterView, self).form_valid(form)
        user = form.auth_user()
        if user:
            login(self.request, user)
        return ret
