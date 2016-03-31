from django.shortcuts import redirect, get_object_or_404
from .models import Redirection


def short_url(request, short_name):
    redir = get_object_or_404(Redirection, name=short_name)
    return redirect(redir.target)
