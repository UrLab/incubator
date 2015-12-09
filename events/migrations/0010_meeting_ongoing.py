# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_event_interested'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='ongoing',
            field=models.BooleanField(default=False),
        ),
    ]
