# myapp/apps.py
from django.apps import AppConfig


class WikiConfig(AppConfig):
    name = 'wiki'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Article'))
