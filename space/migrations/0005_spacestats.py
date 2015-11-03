# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0004_remove_macadress_hidden'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('adress_count', models.IntegerField()),
                ('user_count', models.IntegerField()),
                ('unknown_mac_count', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
