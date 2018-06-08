# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from storage.models import StorageUnit
from django.conf import settings
from slugify import slugify
import os


class Topic(models.Model):
	name = models.CharField(max_length=200)
	enabled = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)


class Algorithm(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	generate_mosaic = models.BooleanField(default=False)
	multitemporal = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='algorithm_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)

	def obtain_versions(self):
		return Version.objects.filter(algorithm_id=self.id)

	def last_version(self):
		return Version.objects.filter(algorithm_id=self.id).last()

	def last_version_no_obsolete(self):
		return Version.objects.filter(algorithm_id=self.id).exists()

	def version_count(self):
		return self.obtain_versions().count()

	def last_version_status(self):
		return self.last_version().get_publishing_state_display()

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
			("can_view_ratings", "Ver listado de calificaciones de una versión de un algoritmo"),
		)


def upload_to(new_version, filename):
	slug_algorithm_name = slugify(new_version.algorithm.name)
	version_name = new_version.number
	filename = "{}_{}.py".format(slug_algorithm_name, version_name)
	full_url = "{}/algorithms/{}/{}".format(settings.MEDIA_ROOT, slug_algorithm_name, filename)
	# deleting the old file if there is any to replace when updating
	try:
		os.remove(full_url)
	except:
		pass
	return full_url


class Version(models.Model):
	DEVELOPED_STATE = '1'
	PUBLISHED_STATE = '2'
	DEPRECATED_STATE = '3'
	# PUBLISHING STATES
	VERSION_STATES = (
		(DEVELOPED_STATE, "EN DESARROLLO"),
		(PUBLISHED_STATE, "PUBLICADA"),
		(DEPRECATED_STATE, "OBSOLETA"),
	)
	algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
	source_storage_units = models.ManyToManyField(StorageUnit, through='VersionStorageUnit')
	description = models.TextField()
	number = models.CharField(max_length=200)
	repository_url = models.CharField(max_length=300)
	source_code = models.FileField(upload_to=upload_to, max_length=1000, blank=True, null=True)
	publishing_state = models.CharField(max_length=2, choices=VERSION_STATES)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='version_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {} - {}".format(self.id, self.algorithm.name, self.number)

	def new_minor_version(self):
		current_version = self.algorithm.last_version().number
		current_major_version = int(current_version.split('.')[0])
		current_minor_version = int(current_version.split('.')[1])
		return "{}.{}".format(current_major_version, current_minor_version + 1)

	def new_major_version(self):
		current_version = self.algorithm.last_version().number
		current_major_version = int(current_version.split('.')[0])
		return "{}.{}".format(current_major_version + 1, 0)

	def count_parameters(self):
		return Parameter.objects.filter(version=self.id).count()


class VersionStorageUnit(models.Model):
	version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='source_version')
	storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, related_name='source_storage_unit')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.storage_unit.name



class Parameter(models.Model):
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

	def __unicode__(self):
		return "{}".format(self.name)
