# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from algorithm.models import Version, Algorithm, Parameter
from django.db.models import Q
import datetime
from django.core.exceptions import ValidationError
from django.conf import settings

class Execution(models.Model):
	ENQUEUED_STATE = '1'
	EXECUTING_STATE = '2'
	ERROR_STATE = '3'
	COMPLETED_STATE = '4'
	CANCELED_STATE = '5'
	EXECUTION_STATES = (
		(ENQUEUED_STATE, "EN ESPERA"),
		(EXECUTING_STATE, "EN EJECUCIÓN"),
		(ERROR_STATE, "CON FALLO"),
		(COMPLETED_STATE, "FINALIZADA"),
		(CANCELED_STATE, "CANCELADA"),
	)
	version = models.ForeignKey(Version, on_delete=models.CASCADE)
	description = models.TextField(blank=True, null=True)
	state = models.CharField(max_length=2, choices=EXECUTION_STATES)
	started_at = models.DateTimeField(blank=True, null=True)
	finished_at = models.DateTimeField(blank=True, null=True)
	trace_error = models.TextField(blank=True, null=True)
	results_available = models.BooleanField(default=False)
	results_deleted_at = models.DateTimeField(blank=True, null=True)
	email_sent = models.BooleanField(default=False)
	executed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='execution_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	generate_mosaic = models.BooleanField(default=True)


	def __unicode__(self):
		return "{} - {} - v{}".format(self.id, self.version.algorithm.name, self.version.number)

	def can_rate(self):
		return False if Review.objects.filter(execution=self, reviewed_by=self.executed_by).count() > 0 else True

	def pending_executions(self):
		return Execution.objects.filter(Q(state=Execution.ENQUEUED_STATE) & Q(created_at__lt=self.created_at))

	class Meta:
		permissions = (
			("can_list_executions", "Ver listado de ejecuciones"),
			("can_view_execution_detail", "Ver detalle de una ejecución"),
			("can_download_execution_results", "Descargar los resultados de la ejecución"),
			("can_rate_execution", "Calificar el resultado de una ejecución"),
			("can_view_blank_execution", "Ver listado de algoritmos para ejecutar"),
			("can_create_new_execution", "Registrar la ejecución de un algoritmo"),
			("can_view_new_execution", "Ver detalle y parámetros de un algoritmo para ejecutar"),
		)


class ExecutionParameter(models.Model):
	execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
	parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def obtain_value(self):
		parameter_type = self.parameter.parameter_type
		response = "Parámetro no soportado"
		if parameter_type == "1":
			response = "{}".format(self.stringtype.value)
		elif parameter_type == "2":
			response = "{}".format(self.integertype.value)
		elif parameter_type == "3":
			response = "{}".format(self.doubletype.value)
		elif parameter_type == "4":
			response = "{}".format(self.booleantype.value)
		elif parameter_type == "7":
			response = "{}, {} - {}, {}".format(self.areatype.latitude_start, self.areatype.longitude_start,
			                                    self.areatype.latitude_end, self.areatype.longitude_end)
		elif parameter_type == "8":
			response = "{}, {}".format(self.storageunitbandtype.storage_unit_name, self.storageunitbandtype.bands)
		elif parameter_type == "9":
			response = "{} - {}".format(self.timeperiodtype.start_date.strftime("%Y-%m-%d"), self.timeperiodtype.end_date.strftime("%Y-%m-%d"))
		elif parameter_type == "12":
			response = "{}".format(self.filetype.file_name())
		elif parameter_type == "13":
			response = "{}".format(self.storageunitnobandtype.storage_unit_name)
		return response

	def obtain_json_values(self):
		parameter_type = self.parameter.parameter_type
		response = "Parámetro no soportado"
		if parameter_type == "1":
			response = {
				'function_name': self.parameter.function_name,
				'value': "{}".format(self.stringtype.value),
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "2":
			response = {
				'function_name': self.parameter.function_name,
				'value': self.integertype.value,
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "3":
			response = {
				'function_name': self.parameter.function_name,
				'value': self.doubletype.value,
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "4":
			response = {
				'function_name': self.parameter.function_name,
				'value': "{}".format(self.booleantype.value),
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "7":
			response = {
				'function_name': self.parameter.function_name,
				'latitude_start': self.areatype.latitude_start,
				'longitude_start': self.areatype.longitude_start,
				'latitude_end': self.areatype.latitude_end,
				'longitude_end': self.areatype.longitude_end,
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "8":
			response = {
				'function_name': self.parameter.function_name,
				'storage_unit_name': "{}".format(self.storageunitbandtype.storage_unit_name),
				'bands': "{}".format(self.storageunitbandtype.bands),
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "9":
			response = {
				'function_name': self.parameter.function_name,
				'start_date': "{}".format(self.timeperiodtype.start_date.strftime('%d-%m-%Y')),
				'end_date': "{}".format(self.timeperiodtype.end_date.strftime('%d-%m-%Y')),
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "12":
			response = {
				'function_name': self.parameter.function_name,
				'value': "{}".format(self.filetype.file_dir()),
				'type': self.parameter.parameter_type,
			}
		elif parameter_type == "13":
			response = {
				'function_name': self.parameter.function_name,
				'storage_unit_name': self.storageunitnobandtype.storage_unit_name,
				'type': self.parameter.parameter_type,
			}
		response['parameter_pk'] = self.parameter.pk
		response['parameter_type'] = self.parameter.parameter_type
		return response

	def __unicode__(self):
		return "{} - {} - {}".format(self.execution.id, self.parameter.get_parameter_type_display(), self.parameter.name)


class StringType(ExecutionParameter):
	value = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.value)


class IntegerType(ExecutionParameter):
	value = models.IntegerField()

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.value)


class DoubleType(ExecutionParameter):
	value = models.FloatField()

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.value)


class BooleanType(ExecutionParameter):
	value = models.BooleanField(default=False)

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.value)


class AreaType(ExecutionParameter):
	latitude_start = models.CharField(max_length=200)
	latitude_end = models.CharField(max_length=200)
	longitude_start = models.CharField(max_length=200)
	longitude_end = models.CharField(max_length=200)

	def __unicode__(self):
		return "{}".format(self.execution.id)


class StorageUnitBandType(ExecutionParameter):
	storage_unit_name = models.CharField(max_length=200)
	bands = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.storage_unit_name)


class StorageUnitNoBandType(ExecutionParameter):
	storage_unit_name = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.storage_unit_name)


class TimePeriodType(ExecutionParameter):
	start_date = models.DateField()
	end_date = models.DateField()

	def __unicode__(self):
		return "{}".format(self.execution)

def validate_file_extension(archivo):
	valid_extensions = ('.zip',)
	if not archivo.name.endswith(valid_extensions) in valid_extensions:
		raise ValidationError(u'Unsupported file extension.')

def get_upload_to(instance, filename):
	return "input/{}/{}/{}".format(instance.execution.id, instance.parameter.name, filename)


class FileType(ExecutionParameter):
	file = models.FileField(upload_to=get_upload_to, validators=[validate_file_extension])

	def file_name(self):
		return self.file.name.split('/')[-1]

	def file_dir(self):
		separated_route = self.file.name.split('/')
		separated_route.insert(0,settings.MEDIA_ROOT)
		file_directory = "/".join(separated_route[:-1])
		return file_directory

	def __unicode__(self):
		return "{}".format(self.file.name)


class MultipleChoiceListType(ExecutionParameter):
	value = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.value)


class Review(models.Model):
	algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
	version = models.ForeignKey(Version, on_delete=models.CASCADE)
	execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
	rating = models.IntegerField()
	comments = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_author')

	def __unicode__(self):
		return "{} - {}".format(self.execution.id, self.rating)


class Task(models.Model):
	PENDING_STATE = '1'
	RECEIVED_STATE = '2'
	STARTED_STATE = '3'
	SUCCESS_STATE = '4'
	FAILURE_STATE = '5'
	REVOKED_STATE = '6'
	RETRY_STATE = '7'
	TASK_STATES = (
		(PENDING_STATE, "PENDIENTE"),
		(RECEIVED_STATE, "RECIBIDO"),
		(STARTED_STATE, "INICIADO"),
		(SUCCESS_STATE, "EXITOSO"),
		(FAILURE_STATE, "CON FALLO"),
		(REVOKED_STATE, "ANULADO"),
		(RETRY_STATE, "REINTENTO"),
	)
	execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
	uuid = models.CharField(max_length=100)
	start_date = models.DateTimeField(blank=True, null=True)
	end_date = models.DateTimeField(blank=True, null=True)
	state = models.CharField(max_length=2, choices=TASK_STATES)
	state_updated_at = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.execution.id, self.uuid)


class FileConvertionTask(models.Model):
	SCHEDULED_STATE = '1'
	EXECUTING_STATE = '2'
	FAILED_STATED = '3'
	COMPLETED_STATE = '4'
	# All the states
	CONVERTION_STATES = (
		(SCHEDULED_STATE, "PROGRAMADA"),
		(EXECUTING_STATE, "EN EJECUCIÓN"),
		(FAILED_STATED, "CON FALLO"),
		(COMPLETED_STATE, "COMPLETADA"),
	)
	execution = models.ForeignKey(Execution, on_delete=models.CASCADE, related_name='execution')
	filename = models.TextField()
	state = models.CharField(max_length=2, choices=CONVERTION_STATES)
	error_messages = models.TextField()
	logs = models.TextField()
	start_execution_date = models.DateTimeField(null=True, blank=True)
	end_execution_date = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('execution', 'filename')