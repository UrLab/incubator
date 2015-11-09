# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151109_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(max_digits=6, verbose_name='ardoise', default=0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='has_key',
            field=models.BooleanField(verbose_name='possède une clé', default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(verbose_name='est administrateur', default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(verbose_name="nom d'utilisateur", unique=True, max_length=30),
        ),
    ]
