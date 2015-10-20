# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('status', models.CharField(max_length=1, choices=[('p', 'proposition'), ('i', 'in progress'), ('f', 'finished')])),
                ('description', models.TextField()),
                ('progress', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('requirements', models.TextField()),
                ('content', models.TextField()),
                ('dependencies', models.ManyToManyField(to='projects.Project', related_name='_dependencies_+', blank=True)),
                ('maintainer', models.ForeignKey(related_name='maintained_projects', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
