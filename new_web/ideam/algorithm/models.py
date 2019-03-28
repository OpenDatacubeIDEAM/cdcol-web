# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from storage.models import StorageUnit

from django.utils.text import slugify


class Topic(models.Model):
    """Algorithms are classified in topics."""

    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Algorithm(models.Model):
    """Metadata considered for an algorithm uploaded by a user."""

    name = models.CharField(max_length=200)
    description = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("can_list_algorithms", "Listar los algoritmos"),
            ("can_create_algorithm", "Crear un algoritmo"),
            ("can_view_algorithm_detail", "Ver detalle de un algoritmo"),
            ("can_edit_algorithm", "Editar algoritmo"),
            ("can_create_new_version", "Crear una nueva versión de un algoritmo"),
            ("can_view_version_detail", "Ver detalle de la versión de un algoritmo"),
            ("can_edit_version", "Editar una versión de un algoritmo"),
            ("can_publish_version", "Publicar versión de un algoritmo"),
            ("can_unpublish_version", "Despublicar versión de un algoritmo"),
            ("can_deprecate_version", "Volver versión de un algoritmo obsoleta"),
            ("can_delete_version", "Eliminar versión de un algoritmo (si no tiene ejecuciones)"),
            ("can_create_parameter", "Crear parámetro para una versión de un algoritmo"),
            ("can_view_parameter_detail", "Ver detalle de un parámetro de una versión de un algoritmo"),
            ("can_edit_parameter", "Editar parámetro de una versión de un algoritmo (tener en cuenta posibles variabilidades por tipo de parámetro)"),
            ("can_view_ratings", "Ver listado de calificaciones de una versión de un algoritmo")
        )


def version_upload_to(instance, filename):
    """File will be uploaded to MEDIA_ROOT/<algo_path>."""
    algo_name = slugify(instance.algorithm.name)
    algo_version_number = instance.number
    filename = '{}_{}.py' % (algo_name,algo_version_number)
    algo_path = 'algorithms/{}/{}' % (algo_name,filename)

    return algo_path

class Version(models.Model):
    """Each algorithm has several versions."""

    DEVELOPED_STATE = '1'
    PUBLISHED_STATE = '2'
    DEPRECATED_STATE = '3'
    REVIEW_PENDING = '4'
    REVIEW = '5'

    VERSION_STATES = (
        (DEVELOPED_STATE, "EN DESARROLLO"),
        (REVIEW_PENDING, 'PENDIENTE DE REVISION'),
        (REVIEW, "EN REVISION"),
        (PUBLISHED_STATE, "PUBLICADA"),
        (DEPRECATED_STATE, "OBSOLETA"),
    )

    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    source_storage_units = models.ManyToManyField(StorageUnit)
    description = models.TextField()
    number = models.CharField(max_length=200)
    repository_url = models.CharField(max_length=300)
    source_code = models.FileField(
        upload_to=version_upload_to,max_length=1000, blank=True, null=True
    )
    publishing_state = models.CharField(max_length=2, choices=VERSION_STATES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("can_list_versions", "Ver listado de Versiones"),
            ("can_send_version_to_review", "Enviar a revisión una versión del algoritmo"),
            ("can_start_version_review", "Iniciar Revisión Versión"),
        )


class VersionStorageUnit(models.Model):
    """Each algorithm version supports a set of storage units (LANDSAT,SENTNEL,etc)."""

    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
