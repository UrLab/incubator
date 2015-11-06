# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0006_auto_20151106_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_open', models.BooleanField()),
            ],
        ),
    ]
