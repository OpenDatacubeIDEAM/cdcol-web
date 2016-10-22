# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from algorithm.models import Version, Algorithm, Parameter


class Execution(models.Model):
	ENQUEUED_STATE = '1'
	EXECUTING_STATE = '2'
	ERROR_STATE = '3'
	COMPLETED_STATE = '4'
	CANCELED_STATE = '5'
	EXECUTION_STATES = (
		(ENQUEUED_STATE, "ENCOLADA"),
		(EXECUTING_STATE, "EN EJECUCIÓN"),
		(ERROR_STATE, "CON FALLO"),
		(COMPLETED_STATE, "COMPLETADA"),
		(CANCELED_STATE, "CANCELADA"),
	)
	version = models.ForeignKey(Version, on_delete=models.CASCADE)
	description = models.TextField()
	state = models.CharField(max_length=2, choices=EXECUTION_STATES)
	started_at = models.DateTimeField()
	finished_at = models.DateTimeField(blank=True, null=True)
	trace_error = models.TextField(blank=True, null=True)
	executed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='execution_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {} - v{}".format(self.id, self.version.algorithm.name, self.version.number)


class ExecutionParameter(models.Model):
	execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
	parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def obtain_value(self):
		parameter_type = self.parameter.parameter_type
		response = "Parámetro no soportado"
		if parameter_type == "7":
			response = "{}, {} - {}, {}".format(self.areatype.latitude_start, self.areatype.longitude_start,
			                                    self.areatype.latitude_end, self.areatype.longitude_end)
		elif parameter_type == "2":
			response = "{}".format(self.integertype.value)
		elif parameter_type == "9":
			response = "{} - {}".format(self.timeperiodtype.start_date, self.timeperiodtype.end_date)
		elif parameter_type == "8":
			response = "{}".format(self.storageunittype.value)
		elif parameter_type == "4":
			response = "{}".format(self.booleantype.value)
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


class StorageUnitType(ExecutionParameter):
	value = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.execution, self.value)


class TimePeriodType(ExecutionParameter):
	start_date = models.DateField()
	end_date = models.DateField()

	def __unicode__(self):
		return "{} - {}".format(self.execution)


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
