# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_transcription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcriptiongamepackage',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
