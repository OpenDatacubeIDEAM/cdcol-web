# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-10 02:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_auto_20160906_2358'),
        ('algorithm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmStorageUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='output_storage_unit',
            field=models.CharField(max_length=200),
        ),
        migrations.AddField(
            model_name='algorithmstorageunit',
            name='algorithm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_algorithm', to='algorithm.Algorithm'),
        ),
        migrations.AddField(
            model_name='algorithmstorageunit',
            name='storage_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_storage_unit', to='storage.StorageUnit'),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='source_storage_units',
            field=models.ManyToManyField(through='algorithm.AlgorithmStorageUnit', to='storage.StorageUnit'),
        ),
    ]
