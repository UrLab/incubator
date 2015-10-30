# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151020_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.CharField(max_length=1000),
        ),
    ]
