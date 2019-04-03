# -*- coding: utf-8 -*-

from django.db import models
from algorithm.models import Version
from django.contrib.auth.models import User


class Execution(models.Model):
    """Algorithms/Workflows execution data."""

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
    executed_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generate_mosaic = models.BooleanField(default=True)
    credits_consumed = models.IntegerField(default=0)

    # def __unicode__(self):
    #     return "{} - {} - v{}".format(self.id, self.version.algorithm.name, self.version.number)

    # def can_rate(self):
    #     return False if Review.objects.filter(execution=self, reviewed_by=self.executed_by).count() > 0 else True

    # def pending_executions(self):
    #     return Execution.objects.filter(Q(state=Execution.ENQUEUED_STATE) & Q(created_at__lt=self.created_at))

    # class Meta:
    #     permissions = (
    #         ("can_list_executions", "Ver listado de ejecuciones"),
    #         ("can_view_execution_detail", "Ver detalle de una ejecución"),
    #         ("can_download_execution_results", "Descargar los resultados de la ejecución"),
    #         ("can_rate_execution", "Calificar el resultado de una ejecución"),
    #         ("can_view_blank_execution", "Ver listado de algoritmos para ejecutar"),
    #         ("can_create_new_execution", "Registrar la ejecución de un algoritmo"),
    #         ("can_view_new_execution", "Ver detalle y parámetros de un algoritmo para ejecutar"),
    #     )


class Review(models.Model):
    """Each execution can be punctuated after it has finished."""

    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_author')