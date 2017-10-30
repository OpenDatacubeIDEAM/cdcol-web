# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from storage.models import StorageUnit


class IngestTask(models.Model):
	SCHEDULED_STATE = '1'
	EXECUTING_STATE = '2'
	FAILED_STATED = '3'
	COMPLETED_STATE = '4'
	# All the states
	INGEST_STATES = (
		(SCHEDULED_STATE, "PROGRAMADA"),
		(EXECUTING_STATE, "EN EJECUCI�N"),
		(FAILED_STATED, "CON FALLO"),
		(COMPLETED_STATE, "COMPLETADA"),
	)
	storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, related_name='ingest_storage_unit')
	state = models.CharField(max_length=2, choices=INGEST_STATES)
	comments = models.TextField()
	error_messages = models.TextField()
	logs = models.TextField()
	start_execution_date = models.DateTimeField(null=True, blank=True)
	end_execution_date = models.DateTimeField(null=True, blank=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingest_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {} - {}".format(self.id, self.storage_unit.name, self.get_state_display())

	class Meta:
		permissions = (
			("can_list_storage_tasks", "Ver listado de tareas de ingesta"),
			("can_create_storage_task", "Programar una nueva tarea de ingesta"),
			("can_view_storage_task_detail", "Ver detalle de una tarea de ingesta"),
		)
