from django.db import models
from datetime import datetime


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nom")
    creator = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    content = models.TextField(verbose_name="Contenu", blank=True)
    nbr_revision = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Article"

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.title
