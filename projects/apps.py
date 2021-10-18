# myapp/apps.py
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Project'))
        registry.register(self.get_model('Task'))
        registry.register(self.get_model('Comment'))
