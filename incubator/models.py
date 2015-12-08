from django.db import models


class ASBLYear(models.Model):
    start = models.DateField(verbose_name='Date de début')
    stop = models.DateField(verbose_name='Date de fin')

    class Meta:
        verbose_name = "Année d'ASBL"


from django.db.models.signals import post_save
from django.dispatch import receiver
from actstream.models import Action
from incubator.lechbot import send_message
from django.conf import settings


@receiver(post_save, sender=Action)
def action_save_handler(sender, created, instance, **kwargs):
    if not created:
        return

    send_message(
        key=type(instance.target).__name__ + "." + instance.verb,
        message="{user} {verb} «{target}» ({url})",
        user=instance.actor,
        verb=instance.verb,
        target=instance.target,
        url=settings.ROOT_URL + instance.target.get_absolute_url()
    )
