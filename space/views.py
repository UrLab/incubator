from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from influxdb import InfluxDBClient

from .djredis import get_redis, get_mac, set_space_open, space_is_open
from .models import MacAdress, SpaceStatus
from .forms import MacAdressForm

from incubator.settings import (STATUS_SECRETS,
                                INFLUX_HOST, INFLUX_PORT, INFLUX_USER,
                                INFLUX_PASS)


def make_pamela():
    redis = get_redis()
    updated, maclist = get_mac(redis)

    known_mac = MacAdress.objects.filter(adress__in=maclist)
    users = {mac.holder for mac in known_mac if mac.holder is not None}

    unknown_mac = list(filter(lambda x: x not in [obj.adress for obj in known_mac], maclist))
    print(maclist)

    return {
        'raw_maclist': maclist,
        'updated': updated,
        'unknown_mac': unknown_mac,
        'users': users,
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

    return render(request, "pamela.html", context)


@csrf_exempt
def status_change(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST is allowed")

    if 'secret' not in request.POST.keys():
        return HttpResponseBadRequest("You must query this endpoint with a secret.")

    if request.POST['secret'] not in STATUS_SECRETS:
        message = 'Bad secret {} is not in the allowed list'.format(request.POST['secret'])
        return HttpResponseForbidden(message)

    if 'open' not in request.POST.keys():
        return HttpResponseBadRequest('You must query this endpoint an "open" key.')

    redis = get_redis()
    state = int(request.POST['open'])
    set_space_open(redis, state)

    return HttpResponse("Hackerspace is now open={}".format(state))


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
    influx_credentials = (INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PASS)
    client = InfluxDBClient(*influx_credentials)
    r = client.query(queries, database="hal")
    return {k: next(v.get_points())['value'] for k, v in zip(sensors, r)}


def spaceapi(request):
    client = get_redis()
    pam = make_pamela()

    names = pam['unknown_mac'] + list(pam['users'])

    if len(names) == 0:
        people_now_present = {
            "value": 0,
        }
    else:
        people_now_present = {
            "value": len(names),
            "names": names,
        }

    response = {
        "api": "0.13",
        "space": "UrLab",
        "logo": "https://urlab.be/urlab.png",
        "url": "https://urlab.be",
        "location": {
            "lat": "50.812915",
            "lon": "4.384396",
            "address": "131, avenue Buyl, 1050, Bruxelles, Belgium",
        },
        "state": {
            "open": space_is_open(client),
            "lastchange": SpaceStatus.objects.last().time.timestamp(),
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
            "value": 100*sensors['light_%s' % loc],
            "unit": '%',
            "location": loc,
            "name": 'light_%s' % loc
        } for loc in ('inside', 'outside')]
    except:
        pass


    return JsonResponse(response)
