# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('status', models.CharField(max_length=1, choices=[('p', 'proposition'), ('i', 'in progress'), ('f', 'finished')])),
                ('description', models.TextField()),
                ('progress', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('requirements', models.TextField()),
                ('content', models.TextField()),
                ('dependencies', models.ManyToManyField(to='projects.Project', related_name='_dependencies_+')),
                ('maintainer', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='maintained_projects')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='projet',
            name='dependencies',
        ),
        migrations.RemoveField(
            model_name='projet',
            name='maintainer',
        ),
        migrations.DeleteModel(
            name='Projet',
        ),
    ]
