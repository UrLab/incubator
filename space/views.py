from django.shortcuts import render
from django.contrib import messages
from .djredis import get_redis, get_mac
from .models import MacAdress
from .forms import MacAdressForm


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
            form = MacAdressForm()
    else:
        form = MacAdressForm()

    context = make_pamela()
    context['form'] = form

    return render(request, "pamela.html", context)
