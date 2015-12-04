# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('incubator', '0001_initial'), ('incubator', '0002_auto_20151103_1439')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ASBLYear',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('start', models.DateField()),
                ('stop', models.DateField()),
            ],
        ),
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
