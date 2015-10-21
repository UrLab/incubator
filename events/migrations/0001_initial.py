# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('place', models.CharField(max_length=300, verbose_name='Localisation', blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='Début', blank=True)),
                ('stop', models.DateTimeField(null=True, verbose_name='Fin', blank=True)),
                ('title', models.CharField(max_length=300, verbose_name='Nom')),
                ('status', models.CharField(choices=[('i', 'En préparation'), ('r', 'Prêt'), ('p', 'Planifié'), ('j', 'Idée')], max_length=1, verbose_name='Etat')),
                ('description', models.TextField(blank=True)),
                ('organizer', models.ForeignKey(verbose_name='Organisateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('OJ', models.TextField()),
                ('PV', models.TextField()),
                ('event', models.ForeignKey(to='events.Event')),
                ('membersPresent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
