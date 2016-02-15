from datetime import timedelta

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

from django_pandas.io import read_frame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from .djredis import get_redis, get_mac, set_space_open, space_is_open
from .models import MacAdress, SpaceStatus, MusicOfTheDay
from .forms import MacAdressForm
from .serializers import PamelaSerializer, SpaceStatusSerializer, MotdSerializer
from .decorators import private_api, one_or_zero
from django.conf import settings


def make_pamela():
    redis = get_redis()
    updated, maclist = get_mac(redis)

    known_mac = MacAdress.objects.filter(adress__in=maclist)
    users = {mac.holder for mac in known_mac if mac.holder is not None}
    visible_users = {u for u in users if not u.hide_pamela}
    unknown_mac = list(filter(lambda x: x not in [obj.adress for obj in known_mac], maclist))

    return {
        'raw_maclist': maclist,
        'updated': updated,
        'unknown_mac': ['xx:xx:xx:xx:' + mac[-5:] for mac in unknown_mac],
        'users': visible_users,
        'hidden': len(users) - len(visible_users),
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
    context['form'] = form
    context['space_open'] = space_is_open(get_redis())
    context['status_change'] = SpaceStatus.objects.last()

    return render(request, "pamela.html", context)


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
    client = InfluxDBClient(*influx_credentials)
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
            "lastchange": SpaceStatus.objects.last().time.timestamp(),
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
            # "phone": "",
            # "keymasters": "";
        },
        "issue_report_channels": [
            "issue_mail",
            "twitter"
        ],
        "sensors": {
            "people_now_present": [people_now_present],
            # "total_member_count": 42,
            # "beverage_supply": [42],
            # "temperature": [],
        },
        # "feeds": {
        #     "calendar": "",
        # },
        "projects": [
            "https://github.com/UrLab",
            "https://urlab.be/projects/",
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
            "value": 100 * sensors['light_%s' % loc],
            "unit": '%',
            "location": loc,
            "name": 'light_%s' % loc
        } for loc in ('inside', 'outside')]
    except:
        pass

    return JsonResponse(response)


def get_openings_df(freq='H', **filter_args):
    # Grab openings in a pandas dataframe
    df = read_frame(SpaceStatus.objects.filter(**filter_args))

    # Drop duplicate time index
    df = df[df.time.diff().dt.total_seconds() > 0]
    df.index = df.time

    # Reindex on a monotonic hourly time index
    index = pd.date_range(start=df.time.min(), end=df.time.max(), freq='H')
    return df.reindex(index, method='pad')


def openings(request):
    query = {}
    if 'from' in request.GET:
        query['time__gte'] = request.GET['from']
    if 'to' in request.GET:
        query['time__lte'] = request.GET['to']

    df = get_openings_df(**query)

    # Group by hour and plot as image
    probs = 100*df.groupby(df.index.time).is_open.mean()
    img = np.repeat([probs], 5, axis=0)
    plt.imshow(img, cmap=plt.cm.RdYlGn, interpolation='none', vmin=0, vmax=100)

    # Put nice ticks, title, etc...
    ticks = np.arange(0, 24, 2)
    plt.xticks(ticks - 0.5, ["%dh" % x for x in ticks])
    plt.yticks([])
    plt.grid()
    f = tuple(x.strftime("%d/%m/%Y") for x in [df.time.min(), df.time.max()])
    plt.title("Proportion d'ouverture de UrLab %s - %s" % f)
    plt.colorbar()

    # Wrap everything in a django response and clear matplotlib context
    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format='png')
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
    queryset = SpaceStatus.objects.all()
    serializer_class = SpaceStatusSerializer


class MotdViewSet(viewsets.ModelViewSet):
    queryset = MusicOfTheDay.objects.all()
    serializer_class = MotdSerializer
