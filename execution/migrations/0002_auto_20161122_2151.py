# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-23 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='execution',
            name='state',
            field=models.CharField(choices=[('1', 'EN ESPERA'), ('2', 'EN EJECUCI\xd3N'), ('3', 'CON FALLO'), ('4', 'FINALIZADA'), ('5', 'CANCELADA')], max_length=2),
        ),
    ]
