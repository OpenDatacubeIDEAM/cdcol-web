# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from storage.models import StorageUnit


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
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='algorithm_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)

	def obtain_versions(self):
		return Version.objects.filter(algorithm_id=self.id)

	def last_version(self):
		return Version.objects.filter(algorithm_id=self.id).last()

	def version_count(self):
		return self.obtain_versions().count()

	def last_version_status(self):
		return self.last_version().get_publishing_state_display()


def upload_to(new_version, filename):
	return "uploads/versions/source_code/{}/{}".format(new_version.id, filename)


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
	source_code = models.FileField(upload_to=upload_to, blank=True, null=True)
	publishing_state = models.CharField(max_length=2, choices=VERSION_STATES)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='version_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {} {}".format(self.id, self.algorithm.name, self.number)

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
		return "{} - {}".format(self.version.name, self.storage_unit.name)


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
	description = models.TextField()
	help_text = models.TextField()
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
