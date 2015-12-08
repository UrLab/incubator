from django.db.models.signals import post_save
from django.dispatch import receiver
from actstream.models import Action
from realtime.helpers import send_message
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
