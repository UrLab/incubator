from django.db.models.signals import post_save
from django.dispatch import receiver
from actstream.models import Action
from realtime.helpers import send_message
from django.conf import settings


@receiver(post_save, sender=Action)
def action_save_handler(sender, created, instance, **kwargs):
    if not created:
        return

    if instance.target:
        send_message(
            key=type(instance.action_object).__name__ + "." + instance.verb,
            message="{user} {verb} «{action_object}» dans «{target}» ({url})",
            user=instance.actor,
            verb=instance.verb,
            action_object=instance.action_object,
            target=instance.target,
            url=settings.ROOT_URL + instance.target.get_absolute_url()
        )
    else:
        send_message(
            key=type(instance.action_object).__name__ + "." + instance.verb,
            message="{user} {verb} «{action_object}» ({url})",
            user=instance.actor,
            verb=instance.verb,
            action_object=instance.action_object,
            url=settings.ROOT_URL + instance.action_object.get_absolute_url()
        )
