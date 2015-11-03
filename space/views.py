from django.shortcuts import render
from .djredis import get_redis, get_mac


def pamela_list(request):
    redis = get_redis()
    updated, maclist = get_mac(redis)

    return render(request, "pamela.html", {"maclist": maclist, "updated": updated})
