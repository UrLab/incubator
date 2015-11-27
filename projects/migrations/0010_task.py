# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0009_auto_20151117_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Nom')),
                ('proposed_on', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('completed_on', models.DateTimeField(null=True, verbose_name='Date de réalisation', blank=True)),
                ('completed_by', models.ForeignKey(null=True, verbose_name='Réalisé par', blank=True, related_name='completed_tasks', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(related_name='tasks', verbose_name='Projet', to='projects.Project')),
                ('proposed_by', models.ForeignKey(related_name='proposed_tasks', verbose_name='Proposé par', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
