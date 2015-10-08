# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151008_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dependencies',
            field=models.ManyToManyField(blank=True, to='projects.Project', related_name='_dependencies_+'),
        ),
        migrations.AlterField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
