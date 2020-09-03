# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-02-06 12:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_article_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Article'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='article',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, verbose_name='Contenu'),
        ),
        migrations.AddField(
            model_name='article',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 2, 6, 12, 14, 51, 793969, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2019, 2, 6, 12, 14, 59, 69165, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='Nom', max_length=200),
        ),
    ]