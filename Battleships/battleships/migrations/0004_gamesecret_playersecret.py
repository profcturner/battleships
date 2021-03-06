# Generated by Django 2.1.1 on 2019-04-02 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battleships', '0003_auto_20190401_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSecret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(max_length=20)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battleships.Game', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSecret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(max_length=20)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battleships.Player', unique=True)),
            ],
        ),
    ]
