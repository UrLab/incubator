import itertools
import traceback
import json

from django.conf import settings
from django.utils import timezone

from realtime import crossbarconnect

if settings.USE_MQTT:
    import paho.mqtt.client as mqtt


def send_message(key, message, *args, **kwargs):
    if settings.USE_WAMP:
        try:
            client = crossbarconnect.Client(
                settings.CROSSBAR_URL,
                secret=settings.CROSSBAR_SECRET,
                key="incubator"
            )

            client.publish(
                topic="incubator.actstream",
                key=key,
                text=message.format(*args, **kwargs),
                time=timezone.now().isoformat(),
            )
        except Exception:
            traceback.print_exc()
            try:
                from raven.contrib.django.raven_compat.models import client
                client.captureException()
            except ImportError:
                print("No Sentry")

    if settings.USE_MQTT:
        try:
            client = mqtt.Client()
            client.connect(settings.MQTT_HOST)
            data = {"key": key, "text": message.format(*args, **kwargs)}
            client.publish("incubator/actstream", json.dumps(data))
        except Exception:
            traceback.print_exc()
            try:
                from raven.contrib.django.raven_compat.models import client
                client.captureException()
            except ImportError:
                print("No Sentry")


def publish_space_state(is_open):
    if is_open:
        text = "Le hackerspace est ouvert ! Rainbows /o/"
    else:
        text = "Le hackerspace est fermé !"

    if settings.USE_WAMP:
        try:
            client = crossbarconnect.Client(
                settings.CROSSBAR_URL,
                secret=settings.CROSSBAR_SECRET,
                key="incubator"
            )
            client.publish(
                'hal.eventstream',
                key='space_status',
                text=text,
                time=timezone.now().isoformat(),
            )
        except Exception:
            traceback.print_exc()
            try:
                from raven.contrib.django.raven_compat.models import client
                client.captureException()
            except ImportError:
                print("No Sentry")

    if settings.USE_MQTT:
        try:
            client = mqtt.Client()
            client.connect(settings.MQTT_HOST)
            data = {"key": "space_status", "text": text}
            client.publish("hal/eventstream", json.dumps(data))
        except Exception:
            traceback.print_exc()
            try:
                from raven.contrib.django.raven_compat.models import client
                client.captureException()
            except ImportError:
                print("No Sentry")


def unique_everseen(iterable, key):
    "List unique elements, preserving order. Remember all elements ever seen."
    seen = set()
    for element in iterable:
        k = key(element)
        if k not in seen:
            seen.add(k)
            yield element


def feed_reducer(stream):
    # We group every action by user
    # Example [A, A, A, B, B, A] will be grouped like [[A, A, A], [B, B], [A]]
    grouped_stream = [list(g) for k, g in itertools.groupby(stream, key=lambda x: x.actor)]

    smaller_stream = []
    for group in grouped_stream:
        # For each group we sort actions by inverse time
        sorted_group = sorted(group, key=lambda x: x.timestamp, reverse=True)

        # And we take only the first one if there are duplicates (actions with same verb and same target)
        unique_group = unique_everseen(sorted_group, key=lambda x: (x.verb, x.action_object))

        smaller_stream.extend(unique_group)

    # We merge every group and sort again by reversed time
    sorted_smaller_stream = sorted(smaller_stream, key=lambda x: x.timestamp, reverse=True)
    return sorted_smaller_stream
