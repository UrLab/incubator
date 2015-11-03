from django.core.management.base import BaseCommand
from space.views import make_pamela
from space.models import SpaceStats


class Command(BaseCommand):
    help = 'Saves some statistics about the space'

    def handle(self, *args, **options):
        data = make_pamela()
        SpaceStats.objects.create(
            adress_count=len(data['raw_maclist']),
            user_count=len(data['users']),
            unknown_mac_count=len(data['unknown_mac'])
        )
