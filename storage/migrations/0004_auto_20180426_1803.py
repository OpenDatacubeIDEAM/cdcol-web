# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-04-26 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_auto_20180426_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageunit',
            name='alias',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]