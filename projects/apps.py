# myapp/apps.py
from django.apps import AppConfig
from actstream import registry


class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        registry.register(self.get_model('Project'))
        registry.register(self.get_model('Task'))
