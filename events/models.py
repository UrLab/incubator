from django.db import models
from django.conf import settings

# Create your models here.
#Events :
#    Des users peuvent participer à un event
#    Les gens peuvnet être "intéressés"
#    Utiliser https://github.com/thoas/django-sequere ?
#    API hackeragenda

class Event(models.Model):
    STATUS_CHOICES = (
        ("i", "in preparation"),
        ("r", "ready"),
        ("p", "planned"),
        ("j", "just an idea"),
    )
    place = models.CharField(max_length=300)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    title = models.CharField(max_length=300)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField()

#    A un OJ et un PV (composés de points)
#    On pourrait créer un pad et le remplir automatiquement puis récupérer le contenu automatiquement après la réu (optionnel)
#    En faire une extension de events : rajouter un pad qui est sychronisé avec la page (inclure un outil d'edit collaborative dans la page direct alors (codé en rust erlang elixir!)?)? Permettrais de créer des notes collaboratives sur nos events.
class Meeting(Event):
    OJ = models.TextField()
    PV = models.TextField()
    membersPresent = models.ManyToManyField(settings.AUTH_USER_MODEL)

