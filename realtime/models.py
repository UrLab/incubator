from django.db.models.signals import post_save
from django.dispatch import receiver
from actstream.models import Action
from realtime.helpers import send_message
from django.conf import settings
# from wiki.models import ArticleRevision
from actstream import action


@receiver(post_save, sender=Action)
def action_save_handler(sender, created, instance, **kwargs):
    is_quiet = instance.data is not None and instance.data.get('quiet', False)
    if not created or is_quiet or not instance.public:
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
        if instance.action_object:
            urltosend = settings.ROOT_URL + instance.action_object.get_absolute_url()
        else:
            urltosend = settings.ROOT_URL
        send_message(
            key=type(instance.action_object).__name__ + "." + instance.verb,
            message="{user} {verb} «{action_object}» ({url})",
            user=instance.actor,
            verb=instance.verb,
            action_object=instance.action_object,
            url=urltosend
        )


"""@receiver(post_save, sender=ArticleRevision)
def wiki_save_handler(sender, created, instance, **kwargs):
    if not created:
        return

    path = str(instance.article.urlpath_set.first())
    # Root node is presented as "(root)" but may be localized
    if path[0] == '(' and path[-1] == ')':
        path = ''
    url = settings.ROOT_URL + "/wiki/" + path

    if url:
        message = "{user} a édité la page «{title}» du wiki ({url})"
    else:
        message = "{user} a créé la page «{title}» sur le wiki"

    send_message(
        key='wiki.revision',
        message=message,
        user=instance.user,
        title=instance.title,
        url=url
    )
    # Add an actream line
    action.send(instance.user, verb='a édité', action_object=instance.article)"""
