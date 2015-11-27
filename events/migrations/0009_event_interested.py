# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_auto_20151126_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='interested',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='interesting_events'),
        ),
    ]
