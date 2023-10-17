from redis import StrictRedis
from space.models import SpaceStatus
from django.conf import settings


def get_redis():
    return StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)


def get_mac(client):
    """Return updated, maclist :
    - updated is the time in seconds since the last update
    - maclist is a list of mac adresses (strings)
    If the key expired, updated = 0 and maclist = []"""

    pipe = client.pipeline()

    pipe.get('incubator_pamela')
    pipe.ttl('incubator_pamela')
    pipe.get('incubator_pamela_expiration')

    mac, ttl, expiration = pipe.execute()

    if mac is None:
        return 0, []

    mac = mac.decode()
    updated = int(expiration) - ttl

    if mac == "":
        return updated, []

    return updated, mac.split(',')


def get_hostnames(client):
    r = client.hgetall("incubator_pamela_hostnames")
    return {k.decode(): v.decode() for k, v in r.items()}


def set_space_open(client, is_open):
    if isinstance(is_open, bool):
        is_open = 1 if is_open else 0
    if is_open > 1:
        is_open = 1

    client.set('incubator_status', is_open)

    SpaceStatus.objects.create(is_open=bool(is_open))


def space_is_open(client) -> bool:
    status = client.get('incubator_status')
    return status is not None and int(status) == 1


if settings.FAKE_REDIS:
    from .fakeredis import *
