# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_auto_20151103_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='macadress',
            name='hidden',
        ),
    ]
