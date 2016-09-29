# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151208_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=1, choices=[('p', 'proposition'), ('i', 'in progress'), ('f', 'finished'), ('a', 'ants are gone')], verbose_name='État'),
        ),
    ]
