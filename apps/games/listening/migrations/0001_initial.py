# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 14:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import listening.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField()),
                ('problem_count', models.IntegerField(default=0)),
                ('average_time_ms', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_history_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('level', models.SmallIntegerField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_text', models.CharField(max_length=200)),
                ('audio_path', models.FileField(upload_to=listening.models.upload_directory)),
                ('level', models.SmallIntegerField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listening.Package')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_time_ms', models.IntegerField()),
                ('failed', models.BooleanField(default=False)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listening.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_problemscore_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]