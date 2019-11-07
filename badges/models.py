from django.db import models
from django.core.urlresolvers import reverse
from incubator import settings

# systeme de badges pour gerer le niveau d'expertise
# division en trois niveaux: initie, disciple, maitre


class Badge(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    hidden = models.BooleanField(default=False)
    icon = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class BadgeWear(models.Model):
    RAC_BID = "RAC"
    INITIATE = "INI"
    DISCIPLE = "DIS"
    MASTER = "MAI"

    LEVEL_CHOICES = (
        (RAC_BID, "Raclure de bidet"),
        (INITIATE, "Initié"),
        (DISCIPLE, "Disciple"),
        (MASTER, "Maître"),
    )

    class Meta:
        unique_together = ("user", "badge")

    badge = models.ForeignKey('Badge')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Utilisateur')
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=RAC_BID)
    action_counter = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    attributor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Attributeur', related_name="attributed")

    def get_absolute_url(self):
        return reverse('badge_view', args=[self.badge.pk])
