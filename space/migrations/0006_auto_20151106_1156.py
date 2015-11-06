# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import space.models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0005_spacestats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macadress',
            name='adress',
            field=models.CharField(unique=True, validators=[space.models.validate_mac], max_length=17, verbose_name='MAC address'),
        ),
        migrations.AlterField(
            model_name='macadress',
            name='machine_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nom de la machine'),
        ),
    ]
