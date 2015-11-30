# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0009_musicoftheday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicoftheday',
            name='day',
            field=models.DateField(unique=True, auto_now_add=True),
        ),
    ]
