# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151020_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 16, 31, 39, 851621, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 16, 31, 42, 715039, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
