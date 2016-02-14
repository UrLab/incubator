from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
import markdown

class Email(models.Model):
    subject = models.CharField(max_length=511, verbose_name="Sujet")
    content = models.TextField(blank=True, verbose_name="Contenu")
    approvers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name="Approbateurs", related_name="approved_emails")
    sent = models.BooleanField(default=False, verbose_name="Envoyé")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def markdown_content(self):
        return mark_safe(markdown.markdown(
            self.content,
            ["nl2br"],
            safe_mode='escape',
            enable_attributes=False,
            output_format="html5"
        ))
