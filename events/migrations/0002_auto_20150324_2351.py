# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('event_ptr', models.OneToOneField(to='events.Event', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('OJ', models.TextField()),
                ('PV', models.TextField()),
                ('membersPresent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=('events.event',),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
