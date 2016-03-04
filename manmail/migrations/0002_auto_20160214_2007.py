# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('manmail', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='members_only',
        ),
        migrations.AlterField(
            model_name='email',
            name='approvers',
            field=models.ManyToManyField(blank=True, related_name='approved_emails', to=settings.AUTH_USER_MODEL, verbose_name='Approbateurs'),
        ),
        migrations.AlterField(
            model_name='email',
            name='sent',
            field=models.BooleanField(default=False, verbose_name='Envoyé'),
        ),
    ]
