# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'poposition'), ('i', 'in progress'), ('f', 'finished')], max_length=1)),
                ('description', models.TextField()),
                ('progress', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('requirement', models.TextField()),
                ('content', models.TextField()),
                ('dependencies', models.ManyToManyField(related_name='dependencies_rel_+', to='projects.Projet')),
                ('maintainer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
