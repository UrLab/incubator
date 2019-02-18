from django.db import models
from django.core.urlresolvers import reverse
from simple_history.models import HistoricalRecords
from datetime import datetime


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nom")
    creator = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    content = models.TextField(verbose_name="Contenu", blank=True)
    nbr_revision = models.IntegerField(default=0)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Article"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_article', args=[self.id])
