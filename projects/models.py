from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import timedelta


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
    title = models.CharField(max_length=300, verbose_name='Nom')

    maintainer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="maintained_projects", verbose_name='Mainteneur')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="État")
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)], verbose_name="Progression")
    dependencies = models.ManyToManyField('self', blank=True, verbose_name="Dépendences")

    picture = models.ImageField(upload_to='project_pictures', null=True, blank=True)

    short_description = models.CharField(max_length=1000, verbose_name="Description courte")
    content = models.TextField(verbose_name="Contenu", blank=True)

    class Meta:
        verbose_name = "Projet"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_project', args=[self.id])

    def is_stalled(self):
        if self.status == "f":
            return False

        stall_time = timezone.now() - self.modified
        month = timedelta(days=30)
        return stall_time > month * 6
