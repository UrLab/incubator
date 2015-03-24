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

