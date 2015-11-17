import urllib
import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.models import Group

from incubator.models import ASBLYear

# Create your models here.
#    User :
#    Des users ont des skills/badges
#    Les badges ne peuvent être donnés que par quelqu'un qui l'a déjà (genre des teachers)
#    un badge pourrait être "utilisateur de la reprap" et "certigfierait" que le user sait utiliser la machine
#    Des users appartiennent à un groupe (anon, registered, membres cotisants, "bureau")
#    Système d'emprunt (optionnel)


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, is_staff=True, **extra_fields)

    def get_by_natural_key(self, username):
        # makes user matching case insensitive
        return self.get(username__iexact=username)


class User(AbstractBaseUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    username = models.CharField(max_length=30, unique=True, verbose_name="nom d'utilisateur")
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=127, blank=True)
    last_name = models.CharField(max_length=127, blank=True)
    is_staff = models.BooleanField(default=False, verbose_name="est administrateur")

    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="ardoise")
    has_key = models.BooleanField(default=False, verbose_name="possède une clé")

    groups = models.ManyToManyField(Group, blank=True)

    def has_module_perms(self, *args, **kwargs):
        return True # TODO : is this a good idea ?

    def has_perm(self, perm_list, obj=None):
        return self.is_staff

    def write_perm(self, obj):
        if self.is_staff:
            return True

        if obj is None:
            return False

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def is_member(self):
        year = ASBLYear.objects.filter(start__gte=timezone.now(), stop__lt=timezone.now())
        return self.membership_set.filter(asbl_year=year).count() > 0

    @property
    def absolute_balance(self):
        return abs(self.balance)

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def gravatar(self):
        default = "http://www.example.com/default.jpg"
        mail = self.email.lower().encode('utf8')
        size = 40
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(mail).hexdigest()

        return gravatar_url


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    asbl_year = models.ForeignKey('incubator.ASBLYear')
