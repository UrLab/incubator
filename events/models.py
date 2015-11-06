from django.db import models
from django.conf import settings
from datetime import timedelta
from django.core.urlresolvers import reverse


# Create your models here.
# Events :
#    Des users peuvent participer à un event
#    Les gens peuvnet être "intéressés"
#    Utiliser https://github.com/thoas/django-sequere ?
#    API hackeragenda


class Event(models.Model):
    STATUS_CHOICES = (
        ("i", "En préparation"),
        ("r", "Prêt"),
        ("p", "Planifié"),
        ("j", "Idée"),
    )
    title = models.CharField(max_length=300, verbose_name='Nom')
    place = models.CharField(max_length=300, verbose_name='Lieu', blank=True)
    start = models.DateTimeField(verbose_name='Date et heure de début', blank=True, null=True)
    stop = models.DateTimeField(verbose_name='Date et heure de fin', blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Etat')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Organisateur')
    description = models.TextField(blank=True)

    def is_only_a_day(self):
        return self.start.date() == self.stop.date()

    def has_no_duration(self):
        return (self.stop - self.start) < timedelta(minutes=5)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_event', args=[self.id])

    class Meta:
        verbose_name = "Événement"

#    A un OJ et un PV (composés de points)
#    On pourrait créer un pad et le remplir automatiquement puis récupérer le contenu automatiquement après la réu (optionnel)
#    En faire une extension de events : rajouter un pad qui est sychronisé avec la page (inclure un outil d'edit collaborative dans la page direct alors (codé en rust erlang elixir!)?)? Permettrais de créer des notes collaboratives sur nos events.


class Meeting(models.Model):
    event = models.OneToOneField(Event, verbose_name="Événement")
    OJ = models.TextField(verbose_name='Ordre du jour')
    PV = models.TextField()
    membersPresent = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Membres présents')

    class Meta:
        verbose_name = "Réunion"
