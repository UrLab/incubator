# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('change_balance', 'Peut modifier son ardoise'),), 'verbose_name': 'Utilisateur'},
        ),
    ]
