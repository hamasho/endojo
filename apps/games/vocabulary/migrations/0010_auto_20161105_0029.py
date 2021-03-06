# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 00:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20161105_0029'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vocabulary', '0009_auto_20161102_2243'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availablepackage',
            unique_together=set([('package', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='packagestate',
            unique_together=set([('user', 'package')]),
        ),
        migrations.AlterUniqueTogether(
            name='translatedword',
            unique_together=set([('word', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='wordstate',
            unique_together=set([('user', 'word')]),
        ),
    ]
