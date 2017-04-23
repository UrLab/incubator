import uuid

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json

from .models import PrivateAPIKey


def one_or_zero(arg):
    """Typecast to 1 or 0"""
    if arg == '1':
        return 1
    elif arg == '0':
        return 0
    raise ValueError("not one or zero")


def private_api(**required_params):
    """
    Filter incoming private API requests, and perform parameter validation and
    extraction
    """
    def outer(some_view):
        @csrf_exempt
        def inner(request, *args, **kwargs):
            if request.method != 'POST':
                return HttpResponseBadRequest(json.dumps({
                    "error": "Only POST requests are allowed",
                    "hint": "Provide a 'secret' POST param with your token",
                }), content_type="application/json")

            if 'secret' not in request.POST.keys():
                return HttpResponseBadRequest(json.dumps({
                    "error": "Missing 'secret' param",
                    "hint": "Provide a 'secret' POST param with your token",
                }), content_type="application/json")

            try:
                uuid.UUID(request.POST['secret'])
            except ValueError:
                message = 'Bad secret {} is not an uuid'.format(
                    request.POST['secret'])
                return HttpResponseBadRequest(json.dumps({
                    "error": message,
                }), content_type="application/json")

            api_key = PrivateAPIKey.objects.filter(key=request.POST['secret'], active=True).first()
            if api_key is None:
                message = 'Bad secret {} is not in the allowed list'.format(
                    request.POST['secret'])
                return HttpResponseForbidden(json.dumps({
                    "error": message,
                }), content_type="application/json")

            params = kwargs
            for name, typecast in required_params.items():
                if name not in request.POST.keys():
                    return HttpResponseBadRequest(json.dumps({
                        "error": "Parameter %s is required" % name,
                    }), content_type="application/json")
                try:
                    params[name] = typecast(request.POST[name])
                except ValueError:
                    return HttpResponseBadRequest(json.dumps({
                        "error": "Did not understand %s=%s" % (name, request.POST[name]),
                        "hint": "Check the type of your parameter ?"
                    }), content_type="application/json")
            response = some_view(request, *args, **params)
            assert response['Content-Type'] == "application/json"
            return response
        return inner
    return outer
