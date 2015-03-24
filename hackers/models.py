from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#    User :
#    Des users ont des skills/badges
#    Les badges ne peuvent être donnés que par quelqu'un qui l'a déjà (genre des teachers)
#    un badge pourrait être "utilisateur de la reprap" et "certigfierait" que le user sait utiliser la machine
#    Des users appartiennent à un groupe (anon, registered, membres cotisants, "bureau")
#    Système d'emprunt (optionnel)

class Hacker(models.Model):
    user = models.OneToOneField(User)
    balance = models.IntegerField(default=0)

class MacAdress(models.Model):
    adress = models.CharField(max_length=17, unique=True)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL)

