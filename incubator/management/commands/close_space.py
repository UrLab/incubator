from django.core.management.base import BaseCommand

from space.djredis import get_redis, set_space_open, space_is_open


class Command(BaseCommand):
    help = "Closes the space automatically everyday at 4a.m."

    def handle(self, *args, **options):
        redis = get_redis()
        if space_is_open(redis):
            set_space_open(redis, False)
