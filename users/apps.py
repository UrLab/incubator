# myapp/apps.py
from django.apps import AppConfig
from actstream import registry


class EventsConfig(AppConfig):
    name = 'user'

    def ready(self):
        registry.register(self.get_model('User'))
