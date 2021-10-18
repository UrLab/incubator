# Generated by Django 3.0.9 on 2020-08-07 00:42

from django.db import migrations, models
import space.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MacAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(max_length=17, unique=True, validators=[space.models.validate_mac], verbose_name='MAC address')),
                ('machine_name', models.CharField(blank=True, max_length=100, verbose_name='Nom de la machine')),
            ],
            options={
                'verbose_name_plural': 'Mac adresses',
            },
        ),
        migrations.CreateModel(
            name='MusicOfTheDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('irc_nick', models.CharField(max_length=200)),
                ('day', models.DateField(auto_now_add=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Musics of the day',
            },
        ),
        migrations.CreateModel(
            name='PrivateAPIKey',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Clef')),
                ('name', models.CharField(max_length=250, verbose_name='Utilisée pour')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': "Clef d'accès à l'API privée",
                'verbose_name_plural': "Clefs d'accès à l'API privée",
            },
        ),
        migrations.CreateModel(
            name='SpaceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=space.models._auto_now)),
                ('is_open', models.BooleanField()),
            ],
            options={
                'verbose_name': "État d'ouverture du Hackerspace",
                'verbose_name_plural': "États d'ouverture du Hackerspace",
            },
        ),
    ]
