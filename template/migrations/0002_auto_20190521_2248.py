# Generated by Django 2.1.7 on 2019-05-21 22:48

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='template/ingest/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('can_list_ingest_templates', 'Ver listado de scritps de generación de metadatos'), ('can_download_metadata_script', 'Descargar scripts de generación de metadatos (.py)')),
            },
        ),
        migrations.CreateModel(
            name='Yaml',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/web_storage'), upload_to='template/yaml/')),
                ('type', models.CharField(choices=[('1', 'DESCRIPCIÓN'), ('2', 'INGESTA')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('can_list_yaml_templates', 'Ver listado de plantillas de archivos YML'), ('can_download_yaml_template', 'Descargar plantilla de archivo YML')),
            },
        ),
        migrations.DeleteModel(
            name='YamlTemplate',
        ),
    ]
