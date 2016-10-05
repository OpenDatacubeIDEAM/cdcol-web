# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from algorithm.models import Version, Parameter


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


class ExecutionParameter(models.Model):
	execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
	parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class StringType(ExecutionParameter):
	value = models.CharField(max_length=200)


class IntegerType(ExecutionParameter):
	value = models.IntegerField()


class BooleanType(ExecutionParameter):
	value = models.BooleanField(default=False)


class AreaType(ExecutionParameter):
	latitude_start = models.CharField(max_length=200)
	latitude_end = models.CharField(max_length=200)
	longitude_start = models.CharField(max_length=200)
	longitude_end = models.CharField(max_length=200)


class StorageUnitType(ExecutionParameter):
	value = models.CharField(max_length=200)


class TimePeriodType(ExecutionParameter):
	start_date = models.DateField()
	end_date = models.DateField()


class MultipleChoiceListType(ExecutionParameter):
	value = models.CharField(max_length=200)
