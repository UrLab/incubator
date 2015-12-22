# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_meeting_ongoing'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'permissions': (('run_meeting', 'Peut mener des réunions'),), 'verbose_name': 'Réunion'},
        ),
    ]
