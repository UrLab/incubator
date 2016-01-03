# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_hide_pamela'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hide_pamela',
            field=models.BooleanField(default=False, verbose_name='caché sur pamela'),
        ),
    ]
