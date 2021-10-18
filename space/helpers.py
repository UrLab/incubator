from django.utils import timezone

from .models import MacAdress
from .djredis import get_redis, space_is_open, get_mac, get_hostnames


from django.conf import settings
from constance import config as dyn_config


def space_may_be_open(instant=None):
    if instant is None:
        instant = timezone.now()

    if instant.weekday() not in settings.OPEN_WEEKDAYS:
        return False

    if instant.hour not in settings.OPEN_HOURS:
        return False

    if not dyn_config.PERIOD_OPEN:
        return False

    return True


def is_stealth_mode():
    return (not space_may_be_open()) and (not space_is_open(get_redis()))


def should_keep(mac):
    return not any([regex.match(mac) for regex in settings.IGNORE_LIST_RE])


def make_pamela():
    redis = get_redis()
    updated, maclist = get_mac(redis)
    hostnames = get_hostnames(redis)

    known_mac = MacAdress.objects.filter(adress__in=maclist)
    users = {mac.holder for mac in known_mac if mac.holder is not None}
    visible_users = {u for u in users if not u.hide_pamela}
    invisible_users = users - visible_users

    # Filter macs that have a MacAdress object in the db
    unknown_mac = filter(lambda x: x not in [obj.adress for obj in known_mac], maclist)

    # Filter macs that are ignored by the regex list
    unknown_mac = [mac for mac in unknown_mac if should_keep(mac)]

    # Match unknown macs to the hostname or hide a part if we don't have a hostname
    unknown_mac = list({hostnames.get(mac, 'xx:xx:xx:xx:' + mac[-5:]) for mac in unknown_mac})

    return {
        'raw_maclist': maclist,
        'updated': updated,
        'unknown_mac': unknown_mac,
        'users': visible_users,
        'hidden_users': invisible_users,
        'hidden': len(invisible_users),
    }


def make_empty_pamela():
    return {
        'raw_maclist': [],
        'updated': 0,
        'unknown_mac': [],
        'users': [],
        'hidden_users': [],
        'hidden': 0,
    }


def user_should_see_pamela(user):
    has_key = user.is_authenticated and user.has_key
    stealth_mode = is_stealth_mode()
    return has_key or user.is_superuser or (not stealth_mode)
