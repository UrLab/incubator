from django.db import models
from incubator import settings
from django.core.exceptions import ValidationError
import re

MAC_REGEX = re.compile(r'([a-f0-9]{2}:){5}[a-f0-9]{2}')


def validate_mac(value):
    if not re.match(MAC_REGEX, value.lower()):
        raise ValidationError("This is not a valid MAC address")


class MacAdress(models.Model):
    adress = models.CharField(max_length=17, unique=True, verbose_name='MAC address', validators=[validate_mac])
    machine_name = models.CharField(blank=True, max_length=100, verbose_name='Nom de la machine')
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.adress = self.adress.lower()
        super(MacAdress, self).save(*args, **kwargs)


class SpaceStatus(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField()


class MusicOfTheDay(models.Model):
    url = models.URLField()
    irc_nick = models.CharField(max_length=200)
    day = models.DateField(auto_now_add=True, unique=True)

    KNOWN_PROVIDERS = {
        'youtube.com': 'youtube',
        'youtu.be': 'youtube',
        'soundcloud.com': 'soundcloud',
    }
