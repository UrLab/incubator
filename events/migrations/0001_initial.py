# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('place', models.CharField(max_length=300)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField()),
                ('title', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('i', 'in preparation'), ('r', 'ready'), ('p', 'planned'), ('j', 'just an idea')], max_length=1)),
                ('organizer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
