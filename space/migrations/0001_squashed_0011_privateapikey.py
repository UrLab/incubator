# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import space.models
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('space', '0001_initial'), ('space', '0002_macadress_machine_name'), ('space', '0003_auto_20151103_1507'), ('space', '0004_remove_macadress_hidden'), ('space', '0005_spacestats'), ('space', '0006_auto_20151106_1156'), ('space', '0007_spacestatus'), ('space', '0008_delete_spacestats'), ('space', '0009_musicoftheday'), ('space', '0010_auto_20151129_2322'), ('space', '0011_privateapikey')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MacAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('adress', models.CharField(validators=[space.models.validate_mac], verbose_name='MAC address', unique=True, max_length=17)),
                ('holder', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('machine_name', models.CharField(max_length=100, verbose_name='Nom de la machine', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpaceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_open', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MusicOfTheDay',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('url', models.URLField()),
                ('irc_nick', models.CharField(max_length=200)),
                ('day', models.DateField(auto_now_add=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateAPIKey',
            fields=[
                ('key', models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='Clef', serialize=False, editable=False)),
                ('name', models.CharField(verbose_name='Utilisée pour', max_length=250)),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "Clefs d'accès à l'API privée",
                'verbose_name': "Clef d'accès à l'API privée",
            },
        ),
    ]
