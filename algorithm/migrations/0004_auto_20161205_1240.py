# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-05 17:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithm', '0003_auto_20161202_2144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='algorithm',
            options={'permissions': (('can_list_algorithms', 'Listar los algoritmos'), ('can_create_algorithm', 'Crear un algoritmo'), ('can_view_algorithm_detail', 'Ver detalle de un algoritmo'), ('can_edit_algorithm', 'Editar algoritmo'), ('can_create_new_version', 'Crear una nueva versi\xf3n de un algoritmo'), ('can_view_version_detail', 'Ver detalle de la versi\xf3n de un algoritmo'), ('can_edit_version', 'Editar una versi\xf3n de un algoritmo'), ('can_publish_version', 'Publicar versi\xf3n de un algoritmo'), ('can_unpublish_version', 'Despublicar versi\xf3n de un algoritmo'), ('can_deprecate_version', 'Volver versi\xf3n de un algoritmo obsoleta'), ('can_delete_version', 'Eliminar versi\xf3n de un algoritmo (si no tiene ejecuciones)'), ('can_create_parameter', 'Crear par\xe1metro para una versi\xf3n de un algoritmo'), ('can_view_parameter_detail', 'Ver detalle de un par\xe1metro de una versi\xf3n de un algoritmo'), ('can_edit_parameter', 'Editar par\xe1metro de una versi\xf3n de un algoritmo (tener en cuenta posibles variabilidades por tipo de par\xe1metro)'), ('can_view_ratings', 'Ver listado de calificaciones de una versi\xf3n de un algoritmo'))},
        ),
    ]
