# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-28 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0011_auto_20180528_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='execution',
            name='credits_consumed',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
