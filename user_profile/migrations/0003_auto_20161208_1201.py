# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-08 17:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_userprofile_is_data_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_analyst',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_data_admin',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_developer',
        ),
    ]
