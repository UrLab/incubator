from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def no_troll_required(func):
    def wrapper(request, *args, **kwargs):
        u = request.user
        if not (u.has_key or u.is_staff) and u.is_troll:
            return render(request, "troll.html")
        return func(request, *args, **kwargs)
    return login_required(wrapper)
