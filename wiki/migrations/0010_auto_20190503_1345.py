# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-05-03 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0009_auto_20190423_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='id',
        ),
        migrations.RemoveField(
            model_name='historicalarticle',
            name='id',
        ),
        migrations.AlterField(
            model_name='article',
            name='nbr_revision',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalarticle',
            name='nbr_revision',
            field=models.IntegerField(blank=True, db_index=True),
        ),
    ]