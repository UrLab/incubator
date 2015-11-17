# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151103_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(verbose_name='Etat', max_length=1, choices=[('r', 'Prêt'), ('i', 'En incubation')]),
        ),
    ]
