# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('events', '0001_initial'), ('events', '0002_auto_20151021_1739'), ('events', '0003_auto_20151103_1439'), ('events', '0004_auto_20151117_1304'), ('events', '0005_auto_20151125_1232'), ('events', '0006_meeting_pad'), ('events', '0007_auto_20151125_1408'), ('events', '0008_auto_20151126_0850'), ('events', '0009_event_interested')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('place', models.CharField(verbose_name='Localisation', blank=True, max_length=300)),
                ('start', models.DateTimeField(verbose_name='Début', blank=True, null=True)),
                ('stop', models.DateTimeField(verbose_name='Fin', blank=True, null=True)),
                ('title', models.CharField(verbose_name='Nom', max_length=300)),
                ('status', models.CharField(verbose_name='Etat', choices=[('i', 'En préparation'), ('r', 'Prêt'), ('p', 'Planifié'), ('j', 'Idée')], max_length=1)),
                ('description', models.TextField(blank=True)),
                ('organizer', models.ForeignKey(verbose_name='Organisateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('OJ', models.TextField()),
                ('PV', models.TextField()),
                ('event', models.OneToOneField(to='events.Event')),
                ('membersPresent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
            field=models.CharField(verbose_name='Lieu', blank=True, max_length=300),
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
            field=models.OneToOneField(verbose_name='Événement', to='events.Event'),
        ),
        migrations.RenameField(
            model_name='meeting',
            old_name='membersPresent',
            new_name='members',
        ),
        migrations.AlterField(
            model_name='meeting',
            name='members',
            field=models.ManyToManyField(verbose_name='Membres présents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(verbose_name='Etat', choices=[('r', 'Prêt'), ('i', 'En incubation')], max_length=1),
        ),
        migrations.AddField(
            model_name='event',
            name='picture',
            field=django_resized.forms.ResizedImageField(upload_to='event_pictures', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='pad',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='OJ',
            field=models.TextField(verbose_name='Ordre du jour', blank=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='PV',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='members',
            field=models.ManyToManyField(verbose_name='Membres présents', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='interested',
            field=models.ManyToManyField(related_name='interesting_events', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
