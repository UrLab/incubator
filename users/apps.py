# myapp/apps.py
from django.apps import AppConfig
from actstream import registry


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        registry.register(self.get_model('User'))



