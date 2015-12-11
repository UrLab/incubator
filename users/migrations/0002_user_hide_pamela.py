# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0009_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hide_pamela',
            field=models.BooleanField(default=True, verbose_name='caché sur pamela'),
        ),
    ]
