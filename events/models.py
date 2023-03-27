from django.db import models
from django.conf import settings
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django_resized import ResizedImageField
import requests


class Event(models.Model):
    STATUS_CHOICES = (
        ("r", "Prêt"),
        ("i", "En incubation"),
    )
    title = models.CharField(max_length=300, verbose_name='Nom')
    place = models.CharField(max_length=300, verbose_name='Lieu', blank=True)
    start = models.DateTimeField(verbose_name='Date et heure de début', blank=True, null=True)
    stop = models.DateTimeField(verbose_name='Date et heure de fin', blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Etat')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Organisateur', on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    picture = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'], quality=100, upload_to='event_pictures', null=True, blank=True, verbose_name="Image")
    interested = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="interesting_events", verbose_name="Personnes intéressées")
    is_talk = models.BooleanField(default=False, verbose_name="Cet événement est une conférence")

    def is_only_a_day(self):
        return self.start.date() == self.stop.date()

    def has_no_duration(self):
        if self.start is None:
            return True
        return (self.stop - self.start) < timedelta(minutes=5)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_event', args=[self.id])

    def get_absolute_full_url(self):
        return settings.ROOT_URL + self.get_absolute_url()

    def is_meeting(self):
        return bool(self.meeting)

    def start_day(self):
        return self.start.replace(hour=0, minute=0, second=0, microsecond=0)

    def is_today_or_before(self):
        if self.start is None:
            return False
        return self.start_day() < timezone.now()

    def is_finished(self):
        instant = self.stop if self.stop else self.start
        if instant is None:
            return False
        return instant < timezone.now()

    def all_day(self):
        return False

    def talks(self):
        if not self.is_talk:
            return None
        lines = self.description.split("\n")
        return [x.strip().strip("#") for x in lines if x.strip().startswith("##")]

    class Meta:
        verbose_name = "Événement"
        ordering = ("start", "stop", )

# A un OJ et un PV (composés de points)
# On pourrait créer un pad et le remplir automatiquement puis récupérer le contenu automatiquement après la réu (optionnel)
# En faire une extension de events : rajouter un pad qui est sychronisé avec la page
# (inclure un outil d'edit collaborative dans la page direct alors (codé en rust erlang elixir!)?)?
# Permettrais de créer des notes collaboratives sur nos events.


class Meeting(models.Model):
    class Meta:
        verbose_name = 'Réunion'
        permissions = (
            ("run_meeting", "Peut mener des réunions"),
        )

    event = models.OneToOneField(Event, verbose_name="Événement", on_delete=models.CASCADE)
    OJ = models.TextField(verbose_name='Ordre du jour', blank=True)
    PV = models.TextField(blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Membres présents', blank=True)
    pad = models.URLField(blank=True)
    ongoing = models.BooleanField(default=False)

    def get_pad_contents(self):
        r = requests.get(self.pad + "/export/txt")
        if r.ok:
            return r.text

    def set_pad_contents(self, content):
        return requests.post(self.pad + "/import", files={'file': ('osef.txt', content)}).ok

    def save(self, *args, **kwargs):
        super(Meeting, self).save(*args, **kwargs)
        if not self.pad:
            self.pad = "https://pad.lqdn.fr/p/urlab-meeting-notes-{}".format(self.id)
        super(Meeting, self).save(*args, **kwargs)
