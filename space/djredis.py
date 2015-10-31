from redis import StrictRedis
from incubator.settings import REDIS_HOST, REDIS_PORT


def get_redis():
    return StrictRedis(REDIS_HOST, REDIS_PORT)


def get_mac(client):
    mac = client.get('incubator_pamela')
    if mac is None:
        return []

    return mac.split(',')
