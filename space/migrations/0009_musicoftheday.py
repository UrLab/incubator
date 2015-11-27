# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0008_delete_spacestats'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicOfTheDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('irc_nick', models.CharField(max_length=200)),
                ('day', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
