# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20151117_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='membersPresent',
            new_name='members',
        ),
        migrations.AddField(
            model_name='event',
            name='picture',
            field=django_resized.forms.ResizedImageField(upload_to='project_pictures', blank=True, null=True),
        ),
    ]
