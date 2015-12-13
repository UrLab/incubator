# myapp/apps.py
from django.apps import AppConfig
from actstream import registry


class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        registry.register(self.get_model('Event'))
        registry.register(self.get_model('Meeting'))
