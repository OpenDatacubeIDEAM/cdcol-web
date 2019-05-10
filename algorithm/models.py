# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from storage.models import StorageUnit


"""
Used to upload file outside the proyect base directory
"""
upload_storage = FileSystemStorage(location=settings.MEDIA_ROOT)


class Topic(models.Model):
    """Algorithms are classified in topics."""

    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """This is the way the object will be rendered in templates."""
        return self.name

    def __unicode__(self):
        """This is the way the object will be rendered in templates."""
        return self.name

    def get_published_algorithms(self):
        """
        Return algorithms which contain versions with 'publishing_state'
        equal to Version.PUBLISHED_STATE. In other words, return algorithms 
        which has some published version.
        """
        return self.algorithm_set.filter(
            version__publishing_state=Version.PUBLISHED_STATE
        )


class Algorithm(models.Model):
    """Algorithm.

    An algorithm is created by a specific user.
    * Only the user that create the algorithm can see it.
    * The DataAdmin can see all created algorithms.
    * An algorithm have serveral Versions.
    """

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

    name = models.CharField(max_length=200)
    description = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """This is the way the object will be rendered in templates."""
        return self.name

    def __unicode__(self):
        """This is the way the object will be rendered in templates."""
        return self.name

    def version_count(self):
        """This is used in algorithm index page."""
        return self.version_set.all().count()

    def last_version_status(self):
        """This is used in algorithm index page."""
        last = self.version_set.all().last()
        if last:
            return last.get_publishing_state_display()
        return ''

    def last_version(self):
        """Return algorithm lattes version.

        This is used when creating a new execution 
        in algorith detail.
        """
        return self.version_set.all().last()

    def next_minor_version(self):
        """Return the next version number for a new algorithm version."""
        
        next_version = '1.0'
        last = self.last_version()
        if last:
            major_number = int(last.number.split('.')[0])
            minor_number = int(last.number.split('.')[1])
            next_version = '{}.{}'.format(major_number,minor_number + 1)

        return next_version

    def next_major_version(self):
        """Return the next version number for a new algorithm version."""
        
        next_version = '1.0'
        last = self.last_version()
        if last:
            major_number = int(last.number.split('.')[0])
            next_version = '{}.{}'.format(major_number + 1,0)

        return next_version




def version_upload_to(instance, filename):
    """File will be uploaded to MEDIA_ROOT/<algo_path>."""

    algo_name = slugify(instance.algorithm.name)
    algo_version_number = instance.number
    filename = '{}_{}.py'.format(algo_name,algo_version_number)
    algo_path = 'algorithms/{}/{}'.format(algo_name,filename)

    return algo_path

class Version(models.Model):
    """Algorithm Version.

    Each algorithm has several versions.
    * Only the owner of the algorithm can (create/update/list) the versions.
    * Only the owner of the algorithm can execute a version while its 
        publishing_state is 'In Development'. 
    * It is only possible to update a version if its publishing_state is in 
        'In Development'.

    This is the life cycle of a given version:

    1. EN DESARROLLO
    2. PENDIENTE DE REVISION
    3. EN REVISION
    4. PUBLICADA
    5. OBSOLETA
    """

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
    source_storage_units = models.ManyToManyField(StorageUnit,through='VersionStorageUnit')
    description = models.TextField()
    number = models.CharField(max_length=200)
    repository_url = models.CharField(max_length=300)
    source_code = models.FileField(
        upload_to=version_upload_to,storage=upload_storage,max_length=1000, blank=True, null=True
    )
    publishing_state = models.CharField(max_length=2, choices=VERSION_STATES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("can_list_versions", "Ver listado de Versiones"),
            ("can_send_version_to_review", "Enviar a revisión una versión del algoritmo"),
            ("can_start_version_review", "Iniciar Revisión Versión"),
        )

    def __str__(self):
        """This is the way the object will be rendered in templates."""
        return '{}-{} ({})'.format(self.algorithm.name,self.number,self.id)

    def __unicode__(self):
        """This is the way the object will be rendered in templates."""
        return '{}-{} ({})'.format(self.algorithm.name,self.number,self.id)


class VersionStorageUnit(models.Model):
    """Each algorithm version supports a set of storage units (LANDSAT,SENTNEL,etc)."""

    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """
        This representation is needed by /static/js/formBuilder.js 
        and admin site.
        """
        return self.storage_unit.alias

    def __str__(self):
        """
        This representation is needed by /static/js/formBuilder.js 
        and admin site.
        """
        return self.storage_unit.alias

class Parameter(models.Model):
    """Algorithm Version Parameter

    Each algorithm version has a set of parameters required by 
    the specific version of the algorithm.
    """

    STRING_TYPE = '1'
    INTEGER_TYPE = '2'
    DOUBLE_TYPE = '3'
    BOOLEAN_TYPE = '4'
    # DATE_TYPE = '5'
    # DATETIME_TYPE = '6'
    AREA_TYPE = '7'
    STORAGE_UNIT_TYPE = '8'
    TIME_PERIOD_TYPE = '9'
    # ONLY_CHOICE_LIST_TYPE = '10'
    # MULTIPLE_CHOICE_LIST_TYPE = '11'
    FILE_TYPE = '12'
    STORAGE_UNIT_SIMPLE_TYPE = '13'
    # full parameter type list
    PARAMETER_TYPES = (
        (STRING_TYPE, "STRING"),
        (INTEGER_TYPE, "INTEGER"),
        (DOUBLE_TYPE, "DOUBLE"),
        (BOOLEAN_TYPE, "BOOLEAN"),
        # (DATE_TYPE, "FECHA"),
        # (DATETIME_TYPE, "FECHA Y HORA"),
        (AREA_TYPE, "AREA"),
        (STORAGE_UNIT_TYPE, "UNIDAD ALMACENAMIENTO CON BANDAS"),
        (TIME_PERIOD_TYPE, "PERIODO DE TIEMPO"),
        # (ONLY_CHOICE_LIST_TYPE, "LISTA DE SELECCIÓN ÚNICA"),
        # (MULTIPLE_CHOICE_LIST_TYPE, "LISTA DE SELECCIÓN MÚLTIPLE"),
        (FILE_TYPE, "ARCHIVO"),
        (STORAGE_UNIT_SIMPLE_TYPE, "UNIDAD ALMACENAMIENTO SIN BANDAS"),
    )

    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    parameter_type = models.CharField(max_length=2, choices=PARAMETER_TYPES)
    description = models.TextField(blank=True, null=True)
    help_text = models.TextField(blank=True, null=True)
    position = models.IntegerField(default=0)
    required = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)
    default_value = models.CharField(max_length=200, default="")
    function_name = models.CharField(max_length=200, default="")
    output_included = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
