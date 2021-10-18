from django.apps import AppConfig


class BadgesConfig(AppConfig):
    name = 'badges'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Badge'))
