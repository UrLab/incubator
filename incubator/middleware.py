from django.http import Http404
from django.urls import reverse


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the requested URL is the admin URL
        if request.path.startswith(reverse('admin:index')):
            # Check if the user is authenticated and is_staff (admin)
            if not request.user.is_authenticated or not request.user.is_staff:
                raise Http404
        return self.get_response(request)
