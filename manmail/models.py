from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
import markdown


class Email(models.Model):
    FOOTER = "_Si vous ne souhaitez pas recevoir cette newsletter," +\
             " changez vos préférences sur " +\
             "[votre profil utilisateur](https://urlab.be/accounts/edit)_"

    subject = models.CharField(max_length=511, verbose_name="Sujet")
    content = models.TextField(blank=True, verbose_name="Contenu")
    approvers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True,
        verbose_name="Approbateurs", related_name="approved_emails")
    sent = models.BooleanField(default=False, verbose_name="Envoyé")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def markdown_content(self):
        content = self.content + "\n" + self.FOOTER
        return mark_safe(markdown.markdown(
            content,
            extensions=["nl2br"],
            safe_mode='escape',
            enable_attributes=False,
            output_format="html5"
        ))
