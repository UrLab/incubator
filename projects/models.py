from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
#    Un projet appartient à des users
#    Un projet peut dépendre d'autres projets (optionnel)
#    Technical requirement (estimation de cout, tout ça) lié à l'inventaire.
#    Vrai système de "gens intéressés" pour vraiment incuber ces putains de projet +1
STATUS_CHOICES = (
    ("p", "poposition"),
    ("i", "in progress"),
    ("f", "finished")
)

class Projet(models.Model):
    maintainer = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    description = models.TextField()
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    dependencies = models.ManyToManyField('self')
    requirement = models.TextField()
    content = models.TextField()

