# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151020_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.TextField(max_length=1000),
        ),
    ]
