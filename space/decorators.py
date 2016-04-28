import uuid

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .models import PrivateAPIKey


def one_or_zero(arg):
    """Typecast to 1 or 0"""
    if arg == '1':
        return 1
    elif arg == '0':
        return 0
    raise ValueError("not one or zero")


def validate(cast, valid=lambda x: True):
    def func(arg):
        r = cast(arg)
        if not valid(r):
            raise ValueError("Invalid value")
        return r
    return func


def private_api(**required_params):
    """
    Filter incoming private API requests, and perform parameter validation and
    extraction
    """
    def outer(some_view):
        @csrf_exempt
        def inner(request, *args, **kwargs):
            if request.method != 'POST':
                return HttpResponseBadRequest("Only POST is allowed")

            if 'secret' not in request.POST.keys():
                return HttpResponseBadRequest(
                    "You must query this endpoint with a secret.")

            try:
                uuid.UUID(request.POST['secret'])
            except ValueError:
                message = 'Bad secret {} is not an uuid'.format(
                    request.POST['secret'])
                return HttpResponseBadRequest(message)

            api_key = PrivateAPIKey.objects.filter(key=request.POST['secret'], active=True).first()
            if api_key is None:
                message = 'Bad secret {} is not in the allowed list'.format(
                    request.POST['secret'])
                return HttpResponseForbidden(message)

            params = kwargs
            for name, typecast in required_params.items():
                if name not in request.POST.keys():
                    return HttpResponseBadRequest(
                        "Parameter %s is required" % name)
                try:
                    params[name] = typecast(request.POST[name])
                except ValueError:
                    return HttpResponseBadRequest(
                        "Did not understood %s=%s" % (name, request.POST[name]))
            return some_view(request, *args, **params)
        return inner
    return outer
