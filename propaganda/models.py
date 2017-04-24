from django.db import models
from django.conf import settings


class Message(models.Model):
    event = models.ForeignKey("events.Event")

    text_fr = models.TextField()
    text_en = models.TextField()
    text_page = models.TextField()

    approvers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="Approbateurs",
        related_name="approved_propaganda_messages"
    )


class FacebookGroup(models.Model):
    name = models.CharField()
    facebook_id = models.CharField()
    lang = models.ChoiceField()
    api_token = models.CharField()


class FacebookGroupPost(models.Model):
    url = models.UrlField()
    message = models.ForeignKey("propaganda.Message")
    group = models.ForeignKey("propaganda.FacebookGroup")


class FacebookPagePost(models.Model):
    url = models.UrlField()
    message = models.ForeignKey("propaganda.Message")
