# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-16 04:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_analyst', models.BooleanField(default=False)),
                ('is_developer', models.BooleanField(default=False)),
                ('institution', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('usage', models.TextField()),
                ('status', models.CharField(choices=[('1', 'POR APROBACI\xd3N'), ('2', 'APROBADO'), ('3', 'RECHAZADO')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
