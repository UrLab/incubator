# Generated by Django 3.0.9 on 2020-09-28 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_auto_20200919_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttransaction',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='souches'),
        ),
    ]
