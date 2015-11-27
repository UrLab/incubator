# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20151125_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='pad',
            field=models.URLField(blank=True),
        ),
    ]
