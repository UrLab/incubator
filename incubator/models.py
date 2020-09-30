from django.db import models


class ASBLYear(models.Model):
    start = models.DateField(verbose_name='Date de début')
    stop = models.DateField(verbose_name='Date de fin')

    class Meta:
        verbose_name = "Année d'ASBL"

    def __str__(self):
        return "{}-{}".format(self.start.year, self.stop.year)
