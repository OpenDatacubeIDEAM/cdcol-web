# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-28 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20180528_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='credits_approved',
            field=models.IntegerField(blank=True, default=8, null=True),
        ),
    ]
