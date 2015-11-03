# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151030_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='macadress',
            name='holder',
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Ardoise'),
        ),
        migrations.AlterField(
            model_name='user',
            name='has_key',
            field=models.BooleanField(default=False, verbose_name='Possède une clé'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Est administrateur'),
        ),
        migrations.DeleteModel(
            name='MacAdress',
        ),
    ]
