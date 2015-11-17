# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20151113_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='project_pictures', null=True),
        ),
    ]
