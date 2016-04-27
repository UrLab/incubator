# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_squashed_0002_auto_20151105_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.TextField(default=''),
        ),
    ]
