# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
import django.core.validators
import django_resized.forms
from django.utils.timezone import utc


class Migration(migrations.Migration):

    replaces = [('projects', '0001_initial'), ('projects', '0002_auto_20151020_1822'), ('projects', '0003_auto_20151020_1824'), ('projects', '0004_auto_20151020_1831'), ('projects', '0005_auto_20151030_1701'), ('projects', '0006_auto_20151103_1439'), ('projects', '0007_project_picture'), ('projects', '0008_auto_20151113_1717'), ('projects', '0009_auto_20151117_1558'), ('projects', '0010_task')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('status', models.CharField(max_length=1, choices=[('p', 'proposition'), ('i', 'in progress'), ('f', 'finished')])),
                ('short_description', models.CharField(max_length=1000)),
                ('progress', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('content', models.TextField()),
                ('dependencies', models.ManyToManyField(to='projects.Project', blank=True, related_name='_dependencies_+')),
                ('maintainer', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='maintained_projects')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 10, 20, 16, 31, 39, 851621, tzinfo=utc))),
                ('modified', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 10, 20, 16, 31, 42, 715039, tzinfo=utc))),
            ],
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Projet'},
        ),
        migrations.AlterField(
            model_name='project',
            name='content',
            field=models.TextField(verbose_name='Contenu'),
        ),
        migrations.AlterField(
            model_name='project',
            name='dependencies',
            field=models.ManyToManyField(to='projects.Project', verbose_name='Dépendences', blank=True, related_name='_dependencies_+'),
        ),
        migrations.AlterField(
            model_name='project',
            name='maintainer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Mainteneur', related_name='maintained_projects'),
        ),
        migrations.AlterField(
            model_name='project',
            name='progress',
            field=models.PositiveIntegerField(verbose_name='Progression', validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.CharField(verbose_name='Description courte', max_length=1000),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(verbose_name='État', max_length=1, choices=[('p', 'proposition'), ('i', 'in progress'), ('f', 'finished')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(verbose_name='Nom', max_length=300),
        ),
        migrations.AddField(
            model_name='project',
            name='picture',
            field=django_resized.forms.ResizedImageField(upload_to='project_pictures', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='content',
            field=models.TextField(verbose_name='Contenu', blank=True),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Nom', max_length=300)),
                ('proposed_on', models.DateTimeField(verbose_name='Date de création', auto_now_add=True)),
                ('completed_on', models.DateTimeField(verbose_name='Date de réalisation', blank=True, null=True)),
                ('completed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Réalisé par', related_name='completed_tasks', null=True)),
                ('project', models.ForeignKey(to='projects.Project', verbose_name='Projet', related_name='tasks')),
                ('proposed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Proposé par', related_name='proposed_tasks')),
            ],
        ),
    ]
