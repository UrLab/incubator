import uuid

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
                return JsonResponse({
                    "error": "Only POST requests are allowed",
                    "hint": "Provide a 'secret' POST param with your token",
                }, status=400)

            if 'secret' not in request.POST.keys():
                return JsonResponse({
                    "error": "Missing 'secret' param",
                    "hint": "Provide a 'secret' POST param with your token",
                }, status=400)

            try:
                uuid.UUID(request.POST['secret'])
            except ValueError:
                message = 'Bad secret {} is not an uuid'.format(
                    request.POST['secret'])
                return JsonResponse({
                    "error": message,
                }, status=400)

            api_key = PrivateAPIKey.objects.filter(key=request.POST['secret'], active=True).first()
            if api_key is None:
                message = 'Bad secret {} is not in the allowed list'.format(
                    request.POST['secret'])
                return JsonResponse({
                    "error": message,
                }, status=403)

            params = kwargs
            for name, typecast in required_params.items():
                if name not in request.POST.keys():
                    return JsonResponse({
                        "error": "Parameter %s is required" % name,
                    }, status=400)
                try:
                    params[name] = typecast(request.POST[name])
                except ValueError:
                    return JsonResponse({
                        "error": "Did not understand %s=%s" % (name, request.POST[name]),
                        "hint": "Check the type of your parameter ?"
                    }, status=400)
            response = some_view(request, *args, **params)
            assert response['Content-Type'] == "application/json"
            return response
        return inner
    return outer
