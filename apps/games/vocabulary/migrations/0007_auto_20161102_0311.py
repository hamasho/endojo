# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0006_auto_20161031_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordstate',
            name='last_appeared',
        ),
        migrations.AddField(
            model_name='wordstate',
            name='added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
