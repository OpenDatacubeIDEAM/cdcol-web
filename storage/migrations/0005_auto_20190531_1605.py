# Generated by Django 2.1.7 on 2019-05-31 21:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_auto_20180426_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageunit',
            name='alias',
            field=models.CharField(default='no definido', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='storageunit',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='storageunit',
            name='root_dir',
            field=models.FilePathField(blank=True, null=True),
        ),
    ]
