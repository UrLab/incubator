from django.db import models


class Redirection(models.Model):
    class Meta:
        verbose_name = "Redirection"
        verbose_name_plural = "Redirections"

    name = models.CharField(max_length=250, unique=True)
    target = models.CharField(max_length=250)

    def __str__(self):
        return "<Redirection {}->{}>".format(self.name, self.target)
