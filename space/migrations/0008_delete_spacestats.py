# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0007_spacestatus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SpaceStats',
        ),
    ]
