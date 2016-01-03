# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0001_squashed_0011_privateapikey'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='macadress',
            options={'verbose_name_plural': 'Mac adresses'},
        ),
        migrations.AlterModelOptions(
            name='musicoftheday',
            options={'verbose_name_plural': 'Musics of the day'},
        ),
        migrations.AlterModelOptions(
            name='spacestatus',
            options={'verbose_name': "État d'ouverture du Hackerspace", 'verbose_name_plural': "États d'ouverture du Hackerspace"},
        ),
    ]
