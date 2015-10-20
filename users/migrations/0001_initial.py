# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=127)),
                ('last_name', models.CharField(max_length=127)),
                ('is_staff', models.BooleanField(default=False)),
                ('balance', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MacAdress',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('adress', models.CharField(max_length=17, unique=True)),
                ('holder', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
