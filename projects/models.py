from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
#    Un projet appartient à des users
#    Un projet peut dépendre d'autres projets (optionnel)
#    Technical requirement (estimation de cout, tout ça) lié à l'inventaire.
#    Vrai système de "gens intéressés" pour vraiment incuber ces putains de projet +1

STATUS_CHOICES = (
    ("p", "proposition"),
    ("i", "in progress"),
    ("f", "finished")
)


class Project(models.Model):
    title = models.CharField(max_length=300)

    maintainer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="maintained_projects")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    dependencies = models.ManyToManyField('self', blank=True)

    short_description = models.CharField(max_length=1000)
    content = models.TextField()
