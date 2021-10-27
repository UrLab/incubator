from django.db import models
from django.urls import reverse
from incubator import settings

# systeme de badges pour gerer le niveau d'expertise
# division en trois niveaux: initie, disciple, maitre


class Badge(models.Model):
    class Meta:
        permissions = (
            ("approve_badge", "Peut approuver une proposition de badge"),
        )

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    hidden = models.BooleanField(default=False)
    icon = models.ImageField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    proposed_by = models.ForeignKey("users.User", verbose_name="initiateur", null=True, blank=True, on_delete=models.PROTECT)
    has_level = models.BooleanField(default=True, verbose_name="Possède des niveaux ?")

    def __str__(self):
        return self.name

    @property
    def userlist(self):
        return [bw.user.username for bw in self.badgewear_set.all()]

    def get_absolute_url(self):
        return reverse('badge_view', args=[self.pk])


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

    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Utilisateur', on_delete=models.CASCADE)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=INITIATE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    attributor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        verbose_name='Attributeur', related_name="attributed",
        on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('badge_view', args=[self.badge.pk])

    def __str__(self):
        return "Badge {} pour {}".format(self.badge.name, self.user.username)
