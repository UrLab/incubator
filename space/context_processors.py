from space.djredis import get_redis, space_is_open


def state(request):
    client = get_redis()
    return {
        "space_open": space_is_open(client),
    }
