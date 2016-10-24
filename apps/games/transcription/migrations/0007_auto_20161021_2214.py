# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0006_auto_20161021_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='level',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='history',
            name='average_time_ms',
            field=models.IntegerField(default=0),
        ),
    ]