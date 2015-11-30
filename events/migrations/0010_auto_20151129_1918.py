# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_event_interested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('r', 'Prêt'), ('i', 'En incubation'), ('o', 'En cours'), ('f', 'Fini')], verbose_name='Etat', max_length=1),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='event',
            field=models.OneToOneField(verbose_name='Événement', to='events.Event', related_name='meeting'),
        ),
    ]
