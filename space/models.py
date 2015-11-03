from django.db import models
from incubator import settings


class MacAdress(models.Model):
    adress = models.CharField(max_length=17, unique=True)
    machine_name = models.CharField(blank=True, max_length=100)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)


class SpaceStats(models.Model):
    adress_count = models.IntegerField()
    user_count = models.IntegerField()
    unknown_mac_count = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
