from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from space.models import PrivateAPIKey


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        if token is None:
            return None
        try:
            api_key = PrivateAPIKey.objects.filter(key=token, active=True).first()
        except ValueError:
            # Badly formed UUID sent
            api_key = None

        if api_key is not None:
            user = api_key.user
        else:
            raise exceptions.AuthenticationFailed('No matching token found.')

        return (user, None)
