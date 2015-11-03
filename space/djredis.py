from redis import StrictRedis
from incubator.settings import REDIS_HOST, REDIS_PORT


def get_redis():
    return StrictRedis(REDIS_HOST, REDIS_PORT)


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
    return updated, mac.split(',')
