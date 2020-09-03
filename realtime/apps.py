# myapp/apps.py
from django.apps import AppConfig


class RealtimeConfig(AppConfig):
    name = 'realtime'

    def ready(self):
        from actstream import registry
        from wiki.models import ArticleRevision, Article
        registry.register(ArticleRevision)
        registry.register(Article)
