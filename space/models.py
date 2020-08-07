from django.db import models
from incubator import settings
from django.core.exceptions import ValidationError
from datetime import datetime
import re
import uuid

MAC_REGEX = re.compile(r'([a-f0-9]{2}:){5}[a-f0-9]{2}')


def validate_mac(value):
    if not re.match(MAC_REGEX, value.lower()):
        raise ValidationError("This is not a valid MAC address")


class MacAdress(models.Model):
    adress = models.CharField(max_length=17, unique=True, verbose_name='MAC address', validators=[validate_mac])
    machine_name = models.CharField(blank=True, max_length=100, verbose_name='Nom de la machine')
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.adress = self.adress.lower()
        super(MacAdress, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Mac adresses"


def _auto_now():
    return datetime.now()


class SpaceStatus(models.Model):
    time = models.DateTimeField(default=_auto_now)
    is_open = models.BooleanField()

    class Meta:
        verbose_name = "État d'ouverture du Hackerspace"
        verbose_name_plural = "États d'ouverture du Hackerspace"


class MusicOfTheDay(models.Model):
    url = models.URLField()
    irc_nick = models.CharField(max_length=200)
    day = models.DateField(auto_now_add=True, unique=True)

    KNOWN_PROVIDERS = {
        'youtube.com': 'youtube',
        'youtu.be': 'youtube',
        'soundcloud.com': 'soundcloud',
    }

    class Meta:
        verbose_name_plural = "Musics of the day"


class PrivateAPIKey(models.Model):
    class Meta:
        verbose_name = "Clef d'accès à l'API privée"
        verbose_name_plural = "Clefs d'accès à l'API privée"

    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='Clef')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Utilisateur', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='Utilisée pour')
    active = models.BooleanField(default=False)

    def __str__(self):
        f = {
            'active': "active" if self.active else "inactive",
            'name': self.name,
            'user': self.user.username
        }
        return '<Private API Key for {user}: "{name}" ({active})>'.format(**f)

    __repr__ = __str__
    __unicode__ = __str__
