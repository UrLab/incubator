import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.urls import reverse
from django.core.exceptions import ValidationError

from rest_framework.authtoken.models import Token

from incubator.models import ASBLYear


def insensitive_unique_username(username):
    # Ceci est un test en prod, pardonnez mon âme.
    # Bisous, c4.
    user = User.objects.filter(username__iexact=username).first()
    if user:
        if user.username == username:
            pass  # We already have database validation for this case
        else:
            raise ValidationError("A user named %s already exists." % username)


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
        return self._create_user(username, email, password, is_superuser=True, **extra_fields)

    def get_by_natural_key(self, username):
        # makes user matching case insensitive
        return self.get(username__iexact=username)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Utilisateur'
        ordering = ['username']
        permissions = (
            ("change_balance", "Peut modifier son ardoise"),
        )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="nom d'utilisateur",
        validators=[insensitive_unique_username]
    )
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=127, blank=True)
    last_name = models.CharField(max_length=127, blank=True)

    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="ardoise")
    has_key = models.BooleanField(default=False, verbose_name="possède une clé")

    hide_pamela = models.BooleanField(default=False, verbose_name='caché sur pamela')
    newsletter = models.BooleanField(default=True, verbose_name='abonné à la newsletter')
    is_active = models.BooleanField(default=True, verbose_name='Utilisateur actif')
    description = models.TextField(default="", verbose_name="Description", max_length=255, null=True)
    discord_id = models.ForeignKey(Token, null=True, blank=True, on_delete=models.CASCADE)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def discord_connected(self):
        return self.discord_id is not None

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_member(self):
        year = ASBLYear.objects.filter(start__gte=timezone.now(), stop__lt=timezone.now())
        return self.membership_set.filter(asbl_year=year).count() > 0

    @property
    def absolute_balance(self):
        return abs(self.balance)

    @property
    def gravatar(self):
        mail = self.email.lower().encode('utf8')
        gravatar_url = "//www.gravatar.com/avatar/" + hashlib.md5(mail).hexdigest() + "?d=wavatar"

        return gravatar_url

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.username])

    def save(self, *args, **kwargs):
        if self.discord_id != "":
            self.discord_id = Token.objects.create(user=self)

        super.save(*args, **kwargs)


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asbl_year = models.ForeignKey('incubator.ASBLYear', on_delete=models.CASCADE)

    def __str__(self):
        return "Membre du hackerspace durant l'année {}".format(self.asbl_year)
