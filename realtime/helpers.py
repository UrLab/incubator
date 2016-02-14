import itertools

from django.conf import settings
from django.utils import timezone

from realtime import crossbarconnect


def send_message(key, message, *args, **kwargs):
    if settings.USE_WAMP:
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
