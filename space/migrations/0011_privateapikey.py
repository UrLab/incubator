# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('space', '0010_auto_20151129_2322'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateAPIKey',
            fields=[
                ('key', models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='Clef', editable=False, serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='Utilisée pour')),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name_plural': "Clefs d'accès à l'API privée",
                'verbose_name': "Clef d'accès à l'API privée",
            },
        ),
    ]
