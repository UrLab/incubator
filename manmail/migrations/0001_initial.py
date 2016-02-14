# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('subject', models.CharField(verbose_name='Sujet', max_length=511)),
                ('content', models.TextField(verbose_name='Contenu', blank=True)),
                ('sent', models.BooleanField(default=False)),
                ('members_only', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('approvers', models.ManyToManyField(related_name='Approbateurs', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
