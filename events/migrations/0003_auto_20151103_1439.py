# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151021_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Événement'},
        ),
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name': 'Réunion'},
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=300, verbose_name='Lieu', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Date et heure de début', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(verbose_name='Date et heure de fin', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='OJ',
            field=models.TextField(verbose_name='Ordre du jour'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='event',
            field=models.OneToOneField(to='events.Event', verbose_name='Événement'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='membersPresent',
            field=models.ManyToManyField(verbose_name='Membres présents', to=settings.AUTH_USER_MODEL),
        ),
    ]
