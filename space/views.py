from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .djredis import get_redis, get_mac, set_space_open
from .models import MacAdress
from .forms import MacAdressForm

from incubator.settings import STATUS_SECRETS


def make_pamela():
    redis = get_redis()
    updated, maclist = get_mac(redis)

    known_mac = MacAdress.objects.filter(adress__in=maclist)
    users = {mac.holder for mac in known_mac if mac.holder is not None}

    unknown_mac = list(filter(lambda x: x not in [obj.adress for obj in known_mac], maclist))

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
