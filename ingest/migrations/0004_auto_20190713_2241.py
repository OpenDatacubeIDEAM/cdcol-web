# Generated by Django 2.1.7 on 2019-07-14 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingest', '0003_auto_20190531_1603'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingesttask',
            options={'ordering': ['-created_at'], 'permissions': (('can_list_storage_tasks', 'Ver listado de tareas de ingesta'), ('can_create_storage_task', 'Programar una nueva tarea de ingesta'))},
        ),
    ]
