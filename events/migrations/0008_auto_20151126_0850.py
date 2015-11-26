# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20151125_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=django_resized.forms.ResizedImageField(null=True, blank=True, upload_to='event_pictures'),
        ),
    ]
