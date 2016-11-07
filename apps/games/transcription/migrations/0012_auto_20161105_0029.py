# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 00:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transcription', '0011_auto_20161029_2025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='packagestate',
            unique_together=set([('user', 'package')]),
        ),
    ]