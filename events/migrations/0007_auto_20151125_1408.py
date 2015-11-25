# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_meeting_pad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='OJ',
            field=models.TextField(blank=True, verbose_name='Ordre du jour'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='PV',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Membres présents'),
        ),
    ]
