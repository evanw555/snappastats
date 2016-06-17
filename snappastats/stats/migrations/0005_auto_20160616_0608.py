# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 06:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20160614_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='DigestedStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.PositiveIntegerField(default=0)),
                ('points', models.PositiveIntegerField(default=0)),
                ('sinks', models.PositiveIntegerField(default=0)),
                ('shots', models.PositiveIntegerField(default=0)),
                ('misses', models.PositiveIntegerField(default=0)),
                ('scorable', models.PositiveIntegerField(default=0)),
                ('throwing_score', models.PositiveSmallIntegerField(default=0)),
                ('catching_score', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='partner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.Player'),
        ),
        migrations.AlterField(
            model_name='player',
            name='scorable',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='team',
            name='opposing_team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.Team'),
        ),
        migrations.AddField(
            model_name='profile',
            name='digested_stats',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.DigestedStats'),
        ),
    ]