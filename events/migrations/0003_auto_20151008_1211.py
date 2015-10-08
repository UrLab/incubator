# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150324_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Organisateur'),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=300, verbose_name='Localisation', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Début', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(max_length=1, verbose_name='Etat', choices=[('i', 'En préparation'), ('r', 'Prêt'), ('p', 'Planifié'), ('j', 'Idée')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(verbose_name='Fin', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Nom'),
        ),
    ]
