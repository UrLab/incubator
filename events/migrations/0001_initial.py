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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('place', models.CharField(max_length=300, verbose_name='Localisation', blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='Début', blank=True)),
                ('stop', models.DateTimeField(null=True, verbose_name='Fin', blank=True)),
                ('title', models.CharField(max_length=300, verbose_name='Nom')),
                ('status', models.CharField(max_length=1, choices=[('i', 'En préparation'), ('r', 'Prêt'), ('p', 'Planifié'), ('j', 'Idée')], verbose_name='Etat')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('event_ptr', models.OneToOneField(to='events.Event', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('OJ', models.TextField()),
                ('PV', models.TextField()),
                ('membersPresent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('events.event',),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(verbose_name='Organisateur', to=settings.AUTH_USER_MODEL),
        ),
    ]
