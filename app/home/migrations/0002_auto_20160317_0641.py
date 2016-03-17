# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 06:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='user_name',
        ),
        migrations.AddField(
            model_name='projects',
            name='project_url',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 17, 6, 41, 4, 613507)),
        ),
    ]
