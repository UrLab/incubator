# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incubator', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asblyear',
            options={'verbose_name': "Année d'ASBL"},
        ),
        migrations.AlterField(
            model_name='asblyear',
            name='start',
            field=models.DateField(verbose_name='Date de début'),
        ),
        migrations.AlterField(
            model_name='asblyear',
            name='stop',
            field=models.DateField(verbose_name='Date de fin'),
        ),
    ]
