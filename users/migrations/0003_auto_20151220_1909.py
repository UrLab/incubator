# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('users', '0002_user_hide_pamela'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_staff',
            new_name='is_superuser',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set', blank=True, related_query_name='user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set', blank=True, related_query_name='user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hide_pamela',
            field=models.BooleanField(default=False, verbose_name='caché sur pamela'),
        ),
    ]
