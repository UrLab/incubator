from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.utils import timezone
from influxdb import InfluxDBClient
from rest_framework import viewsets
from rest_framework.response import Response

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import timedelta

from .djredis import get_redis, get_mac, set_space_open, space_is_open, get_hostnames
from .models import MacAdress, SpaceStatus, MusicOfTheDay
from .forms import MacAdressForm
from .serializers import PamelaSerializer, SpaceStatusSerializer, MotdSerializer
from .decorators import private_api, one_or_zero
from .plots import weekday_plot, weekday_probs, human_time
from users.models import User

from django.conf import settings


def make_pamela():
    redis = get_redis()
    updated, maclist = get_mac(redis)
    hostnames = get_hostnames(redis)

    known_mac = MacAdress.objects.filter(adress__in=maclist)
    users = {mac.holder for mac in known_mac if mac.holder is not None}
    visible_users = {u for u in users if not u.hide_pamela}
    invisible_users = users - visible_users

    unknown_mac = list(filter(lambda x: x not in [obj.adress for obj in known_mac], maclist))

    unknown_mac = [hostnames.get(mac, 'xx:xx:xx:xx:' + mac[-5:]) for mac in unknown_mac]

    return {
        'raw_maclist': maclist,
        'updated': updated,
        'unknown_mac': unknown_mac,
        'users': visible_users,
        'hidden_users': invisible_users,
        'hidden': len(invisible_users),
    }


def pamela_list(request):
    if request.method == 'POST':
        form = MacAdressForm(request.POST)
        if form.is_valid():
            mac = form.save(commit=False)
            mac.holder = request.user
            mac.save()
            messages.success(request, 'Votre MAC a été ajoutée !')

            return HttpResponseRedirect(reverse('pamela_list'))
    else:
        form = MacAdressForm()

    context = make_pamela()
    del context['hidden_users']
    context['form'] = form
    context['space_open'] = space_is_open(get_redis())
    context['status_change'] = SpaceStatus.objects.last()

    return render(request, "pamela.html", context)


@private_api()
def full_pamela(request):
    data = make_pamela()
    pool = list(data['unknown_mac']) + [u.username for u in (data['hidden_users'] | data['users'])]
    return JsonResponse(pool, safe=False)


@private_api(open=one_or_zero)
def status_change(request, open):
    set_space_open(get_redis(), open)
    return HttpResponse("Hackerspace is now open={}".format(open))


@private_api(url=str, nick=str)
def motd_change(request, url, nick):
    MusicOfTheDay.objects.create(url=url, irc_nick=nick)
    return HttpResponse("Music has been changed to {} by {}".format(url, nick))


class DeleteMACView(DeleteView):
    model = MacAdress
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj = super(DeleteMACView, self).get_object()
        if not obj.holder == self.request.user:
            raise PermissionDenied
        return obj


def get_sensors(*sensors):
    query_template = "SELECT value FROM %s ORDER BY time DESC LIMIT 1"
    queries = ';'.join(query_template % s for s in sensors)
    influx_credentials = (settings.INFLUX_HOST, settings.INFLUX_PORT, settings.INFLUX_USER, settings.INFLUX_PASS)
    client = InfluxDBClient(*influx_credentials, timeout=1)
    r = client.query(queries, database="hal")
    if len(sensors) == 1:
        return {sensors[0]: next(r.get_points())['value']}
    else:
        return {k: next(v.get_points())['value'] for k, v in zip(sensors, r)}


@cache_page(30)
def spaceapi(request):
    client = get_redis()
    pam = make_pamela()

    users = [u.username for u in pam['users']]
    names = pam['unknown_mac'] + users

    if len(names) == 0:
        people_now_present = {
            "value": pam['hidden'],
        }
    else:
        people_now_present = {
            "value": len(names) + pam['hidden'],
            "names": names,
        }

    keymasters = [
        {
            'name': user.username,
            # 'irc_nick':,
            # 'email':,
        }
        for user in User.objects.filter(has_key=True)
    ]

    response = {
        "api": "0.13",
        "space": "UrLab",
        "logo": "https://urlab.be/static/img/space-invaders.png",
        "url": "https://urlab.be",
        "location": {
            "lat": 50.812915,
            "lon": 4.384396,
            "address": "131, avenue Buyl, 1050, Bruxelles, Belgium",
        },
        "state": {
            "open": space_is_open(client),
            "lastchange": round(SpaceStatus.objects.last().time.timestamp()),
            "icon": {
                "open": "https://urlab.be/static/img/space-invaders-open.png",
                "closed": "https://urlab.be/static/img/space-invaders.png"
            }
        },
        # "events": {},
        "contact": {
            "issue_mail": "contact@urlab.be",
            "ml": "hackulb@cerkinfo.be",
            "twitter": "@UrLabBxl",
            "facebook": "https://www.facebook.com/urlabbxl",
            "irc": "irc://chat.freenode.net#urlab",
            "email": "contact@urlab.be",
            "phone": "+3226504967",
            "keymasters": keymasters,
        },
        "issue_report_channels": [
            "issue_mail",
            "twitter"
        ],
        "sensors": {
            "people_now_present": [people_now_present],
            # "beverage_supply": [42],
            # "temperature": [],
        },
        # "feeds": {
        #     "calendar": "",
        # },
        "projects": [
            "https://urlab.be/projects/",
            "https://github.com/UrLab",
        ],
    }

    try:
        sensors = get_sensors('light_inside', 'light_outside', 'door_stairs')
        response["sensors"]["door_locked"] = [{
            "value": sensors['door_stairs'] == 0,
            "location": "stairs",
            "name": "door_stairs"
        }]
        response["sensors"]["light"] = [{
            "value": round(100 * sensors['light_%s' % loc], 2),
            "unit": '%',
            "location": loc,
            "name": 'light_%s' % loc
        } for loc in ('inside', 'outside')]
    except:
        pass

    return JsonResponse(response)


def openings_data(request):
    opts = {k: request.GET[k] for k in request.GET}
    return JsonResponse({
        'probs': list(weekday_probs(opts)),
        'range': human_time(opts),
    })


def openings(request):
    opts = {k: request.GET[k] for k in request.GET}

    weekday_plot(plt, opts)

    # Wrap everything in a django response and clear matplotlib context
    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format='png', facecolor=(0, 0, 0, 0),
                edgecolor='none', bbox_inches='tight', pad_inches=0)
    plt.clf()
    return response


class PamelaObject(object):
    def __init__(self, pamela_dict):
        last_updated = timezone.now() - timedelta(seconds=pamela_dict['updated'])

        self.total_mac_count = len(pamela_dict['raw_maclist'])
        self.last_updated = last_updated
        self.age = pamela_dict['updated']
        self.unknown_mac = pamela_dict['unknown_mac']
        self.users = pamela_dict['users']
        self.hidden = pamela_dict['hidden']


class PamelaViewSet(viewsets.ViewSet):
    def list(self, request):
        pam = PamelaObject(make_pamela())
        serializer = PamelaSerializer(pam)
        return Response(serializer.data)


class OpeningsViewSet(viewsets.ModelViewSet):
    queryset = SpaceStatus.objects.all().order_by('-time')
    serializer_class = SpaceStatusSerializer


class MotdViewSet(viewsets.ModelViewSet):
    queryset = MusicOfTheDay.objects.all().order_by('-day')
    serializer_class = MotdSerializer
