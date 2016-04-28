# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='qrcode',
            field=models.TextField(verbose_name='QR Code de la carte de membre', default=''),
        ),
    ]
