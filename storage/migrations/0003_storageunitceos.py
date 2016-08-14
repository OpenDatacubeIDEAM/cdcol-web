# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-06 04:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20160805_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageUnitCEOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_feed', models.FileField(upload_to=b'')),
                ('source_storage_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_storage_unit', to='storage.StorageUnit')),
                ('storage_unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='storage.StorageUnit')),
            ],
        ),
    ]