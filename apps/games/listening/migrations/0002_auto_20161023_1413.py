# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 14:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listening', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='audio_path',
            new_name='audio_file',
        ),
    ]