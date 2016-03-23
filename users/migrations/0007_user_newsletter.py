# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='newsletter',
            field=models.BooleanField(default=True, verbose_name='abonné à la newsletter'),
        ),
    ]
