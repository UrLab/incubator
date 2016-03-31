from django.db.models.signals import post_save
from django.dispatch import receiver
from actstream.models import Action
from realtime.helpers import send_message
from django.conf import settings
from wiki.models import ArticleRevision


@receiver(post_save, sender=Action)
def action_save_handler(sender, created, instance, **kwargs):
    is_quiet = instance.data is not None and instance.data.get('quiet', False)
    if not created or is_quiet:
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


@receiver(post_save, sender=ArticleRevision)
def wiki_save_handler(sender, created, instance, **kwargs):
    if not created:
        return

    path = str(instance.article.urlpath_set.first())
    # Root node is presented as "(root)" but may be localized
    if path[0] == '(' and path[-1] == ')':
        path = ''
    url = settings.ROOT_URL + "/wiki/" + path

    send_message(
        key='wiki.revision',
        message="{user} a édité la page «{title}» du wiki ({url})",
        user=instance.user,
        title=instance.title,
        url=url
    )
