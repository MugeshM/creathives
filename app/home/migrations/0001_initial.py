# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('user_name', models.CharField(max_length=30, null=True, verbose_name='user name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('date_of_birth', models.DateField(null=True)),
                ('contact_number', models.CharField(max_length=30, null=True, blank=True)),
                ('location', models.CharField(max_length=30, null=True)),
                ('gender', models.CharField(max_length=2, null=True, choices=[(b'1', b'Male'), (b'2', b'Female'), (b'3', b'Other')])),
                ('profile_url', models.CharField(max_length=200)),
                ('aboutme', models.CharField(max_length=300)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('activation_key', models.CharField(max_length=40, blank=b'True')),
                ('reset_password_key', models.CharField(max_length=40, blank=b'True')),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2016, 3, 16, 11, 39, 11, 384829))),
                ('is_email_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name=b'user', related_name='tmp_user_set', verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name=b'user', related_name='tmp_user_set', verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'db_table': 'creativesaccount',
            },
        ),
        migrations.CreateModel(
            name='projects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_title', models.CharField(max_length=100)),
                ('project_desc', models.CharField(max_length=350)),
                ('user_name', models.CharField(max_length=100)),
                ('posted_date', models.DateTimeField(verbose_name=b'date posted')),
                ('thumbnail_url', models.CharField(max_length=200)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
