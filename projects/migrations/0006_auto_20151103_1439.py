# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20151030_1701'),
    ]

    operations = [
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
            field=models.ManyToManyField(related_name='_dependencies_+', verbose_name='Dépendences', blank=True, to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='maintainer',
            field=models.ForeignKey(related_name='maintained_projects', to=settings.AUTH_USER_MODEL, verbose_name='Mainteneur'),
        ),
        migrations.AlterField(
            model_name='project',
            name='progress',
            field=models.PositiveIntegerField(verbose_name='Progression', validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.CharField(max_length=1000, verbose_name='Description courte'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=1, verbose_name='État', choices=[('p', 'proposition'), ('i', 'in progress'), ('f', 'finished')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Nom'),
        ),
    ]
