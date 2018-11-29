from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import timedelta
from django_resized import ResizedImageField


# Create your models here.
#    Un projet appartient à des users
#    Un projet peut dépendre d'autres projets (optionnel)
#    Technical requirement (estimation de cout, tout ça) lié à l'inventaire.
#    Vrai système de "gens intéressés" pour vraiment incuber ces putains de projet +1

User = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
    ("p", "proposition"),
    ("i", "in progress"),
    ("f", "finished"),
    ("a", "ants are gone"),
)


class Project(models.Model):
    ANT_CHAR = u"\U0001F41C"

    title = models.CharField(max_length=300, verbose_name='Nom')

    maintainer = models.ForeignKey(User, related_name="maintained_projects", verbose_name='Mainteneur')
    participants = models.ManyToManyField(User, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="État")
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)], verbose_name="Progression")
    dependencies = models.ManyToManyField('self', blank=True, verbose_name="Dépendences")

    picture = ResizedImageField(size=[500, 500], upload_to='project_pictures', null=True, blank=True)

    short_description = models.CharField(max_length=1000, verbose_name="Description courte")
    content = models.TextField(verbose_name="Contenu", blank=True)

    likes = models.ManyToManyField(User, related_name ="likes")

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


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', verbose_name='Projet')
    name = models.CharField(max_length=300, verbose_name='Nom')

    proposed_by = models.ForeignKey(User, related_name='proposed_tasks', verbose_name='Proposé par')
    proposed_on = models.DateTimeField(verbose_name='Date de création', auto_now_add=True)

    completed_by = models.ForeignKey(User, related_name='completed_tasks', verbose_name='Réalisé par', null=True, blank=True)
    completed_on = models.DateTimeField(verbose_name='Date de réalisation', null=True, blank=True)

    @property
    def completed(self):
        return self.completed_by is not None

    def save(self, *args, **kwargs):
        self.project.save()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
