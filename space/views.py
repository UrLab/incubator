from django.shortcuts import render
from .djredis import get_redis, get_mac
from .models import MacAdress


def pamela_list(request):
    redis = get_redis()
    updated, maclist = get_mac(redis)

    known_mac = MacAdress.objects.filter(adress__in=maclist)
    unknown_mac = filter(lambda x: x not in [obj.adress for obj in known_mac], maclist)
    users = {mac.holder for mac in known_mac if mac.holder is not None}

    return render(request, "pamela.html", {
        "unknown_mac": unknown_mac,
        "users": users,
        "updated": updated
    })
