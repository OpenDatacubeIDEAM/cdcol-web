# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-05 23:25
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_unit_type', models.CharField(max_length=200)),
                ('processing_level', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('file_description', models.CharField(max_length=200)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField()),
                ('root_dir', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StorageUnitCDCOL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailed_processing_level', models.CharField(max_length=200)),
                ('storage_unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='storage.StorageUnit')),
            ],
        ),
    ]