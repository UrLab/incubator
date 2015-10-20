# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='description',
            new_name='short_description',
        ),
        migrations.RemoveField(
            model_name='project',
            name='requirements',
        ),
    ]
