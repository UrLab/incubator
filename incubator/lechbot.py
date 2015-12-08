from django.conf import settings
from django.utils import timezone

from incubator import crossbarconnect


def send_message(key, message, *args, **kwargs):
    if settings.USE_WAMP:
        client = crossbarconnect.Client(settings.CROSSBAR_URL, secret=settings.CROSSBAR_SECRET, key="Much key")

        client.publish(
            topic="incubator.actstream",
            key=key,
            text=message.format(*args, **kwargs),
            time=timezone.now().isoformat(),
        )
