# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    replaces = [('users', '0001_initial'), ('users', '0002_auto_20151030_1628'), ('users', '0003_auto_20151103_1439'), ('users', '0004_auto_20151109_1358'), ('users', '0005_auto_20151109_1455'), ('users', '0006_auto_20151113_1450'), ('users', '0007_user_groups'), ('users', '0008_auto_20151117_1304'), ('users', '0009_user_is_active')]

    dependencies = [
        ('incubator', '__first__'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name="nom d'utilisateur")),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=127, blank=True)),
                ('last_name', models.CharField(max_length=127, blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='est administrateur')),
                ('balance', models.DecimalField(decimal_places=2, default=0, verbose_name='ardoise', max_digits=6)),
                ('has_key', models.BooleanField(default=False, verbose_name='possède une clé')),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('asbl_year', models.ForeignKey(to='incubator.ASBLYear')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
