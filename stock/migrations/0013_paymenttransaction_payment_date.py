# Generated by Django 3.0.9 on 2020-09-28 22:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_paymenttransaction_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransaction',
            name='payment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]