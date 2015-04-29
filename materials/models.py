from django.db import models
from django.conf import settings

# Create your models here.
class Material(models.Model):
    name = models.CharField(max_length=100) # Make this unique?
    quantity = models.IntegerField(default=1)

class Borrow(models.Model):
    borrower = models.OneToOneField(settings.AUTH_USER_MODEL)
    material = models.OneToOneField(Material)
    quantity = models.IntegerField(default=1)
