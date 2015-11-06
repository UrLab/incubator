from django.shortcuts import render
from space.djredis import get_redis, space_is_open


def home(request):
    client = get_redis()
    return render(request, "home.html", {
        "space_open": space_is_open(client)
    })
