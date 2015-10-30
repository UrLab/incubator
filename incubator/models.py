from django.db import models


class ASBLYear(models.Model):
    start = models.DateField()
    stop = models.DateField()
