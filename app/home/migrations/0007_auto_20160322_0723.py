# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 07:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20160322_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='posted_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date posted'),
        ),
        migrations.AlterField(
            model_name='user',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 22, 7, 23, 9, 978710)),
        ),
    ]
