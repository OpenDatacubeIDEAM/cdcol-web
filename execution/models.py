# -*- coding: utf-8 -*-

from django.db import models
from algorithm.models import Version
from algorithm.models import Parameter
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import formats
from django.utils import timezone

from airflow.models import DagRun

import os


"""
Used to upload file outside the proyect base directory
"""
upload_storage = FileSystemStorage(location=settings.MEDIA_ROOT)


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

    AIRFLOW_STATES = {
        'running': "EN EJECUCIÓN",
        'success': "FINALIZADA",
        'failed': "CON FALLO"
    }

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
        ordering = ['-pk']


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
    # Not used
    generate_mosaic = models.BooleanField(default=True)
    credits_consumed = models.IntegerField(default=0)
    dag_id = models.CharField(max_length=1000,default='no_definido')

    def get_dag_run(self):
        """
        Return the last dag run associated with
        the dag_id from airflow database.

        NOTE: If the execution is not in ERROR_STATE
        the dag run is not retrieved form airflow.
        """

        # Possible known execption
        # sqlalchemy.exc.OperationalError:
        # (sqlite3.OperationalError) no such table: dag_run
        # when the ariflow data base is not set correctly
        #try:
            #if not self.finished_at == self.state and self.dag_id:
            #    dag_runs = DagRun.find(dag_id=self.dag_id)
            #    if dag_runs:
            #        return dag_runs[-1]

        #except Exception as e:
        #    pass

        return None

    def get_task_instances(self,state):

        try:
            if self.dag_id:
                dag_runs = DagRun.find(dag_id=self.dag_id)
                if dag_runs:
                    dag_run = dag_runs[-1]
                    return dag_run.get_task_instances(state=state)
        except Exception as e:
            pass

        return []

    def to_web_state(self,state):
        return Execution.AIRFLOW_STATES.get(state,'No defiido')

    def get_state(self):

        # To cacth get_dag_run() execption in 
        # case airflow database is not present

        dag_state = self.get_state_display()
        dag_run = self.get_dag_run()
        if dag_run:
            dag_state = self.to_web_state(dag_run.state)

        return dag_state

    def get_created_at(self):
        date = self.created_at
        if date:
            date = timezone.localtime(date)
            date = formats.date_format(
                date,format="DATETIME_FORMAT"
            )
            return date
        return date

    def get_started_at(self):

        date = self.started_at
        if date:
            date = timezone.localtime(date)
            date = formats.date_format(date,format="DATETIME_FORMAT")

        dag_run = self.get_dag_run()
        if dag_run:
            start_date = dag_run.start_date
            if start_date:
                # If time is form airflow, it must be converted form 
                # UTC time to colombiand time. 
                date = timezone.localtime(start_date)
                date = formats.date_format(date,format="DATETIME_FORMAT")

        return date

    def get_finished_at(self):

        date = self.finished_at
        if date:
            date = timezone.localtime(date)
            date = formats.date_format(date,format="DATETIME_FORMAT")

        dag_run = self.get_dag_run()
        if dag_run:
            end_date = dag_run.end_date
            if end_date:
                # If time is form airflow, it must be converted form 
                # UTC time to colombiand time. 
                date = timezone.localtime(end_date)
                date = formats.date_format(date,format="DATETIME_FORMAT")

        return date
        
    def can_rate(self):
        """If the execution was already reviwed it can not be reviwed again.

        This function is used by ExecutionSerializer.
        """
        if self.review_set.filter(reviewed_by=self.executed_by).count() > 0:
            return False
        return True

    def pending_executions(self):
        """
        WARNING: this query depends of the object which perfomrs the query
        created_at__lt=self.created_at

        This function is used by ExecutionSerializer.
        """
        return Execution.objects.filter(
            state=Execution.ENQUEUED_STATE,created_at__lt=self.created_at
        )

    def result_file_path(self):
        """
        Return the file path of the execution result file in
        /web_storage/results/{{dag_id}}/resultado_{{dag_id}}.zip
        """
        results_path = settings.EXECUTION_RESULTS_PATH
        dag_id = self.dag_id or ''
        file_name = 'resultados_{}.zip'.format(dag_id)
        file_path = os.path.join(results_path,dag_id,file_name)
        #if os.path.exists(file_path):
        #    return file_path

        return file_path

    def result_file_path_exists(self):
        """
        Return true if the results file path exists, false otherwise
        """
        file_path = self.result_file_path()
        return os.path.exists(file_path)


class ExecutionParameter(models.Model):
    """Each algorithm version has a set of parameters defined."""
    
    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def obtain_time_range_file(self):
        if self.parameter.parameter_type == "9":
            return "u{}u{}".format(self.timeperiodtype.start_date.strftime("%d-%m-%Y"), self.timeperiodtype.end_date.strftime("%d-%m-%Y"))
        else:
            return "--"

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
        elif parameter_type == "14":
            names = self.multistorageunittype.storage_unit_name.split(';')
            bands = self.multistorageunittype.bands.split(';')
            response = ''
            for storage_name, band in zip(names,bands):
                if band:
                    response += "{}: {}\n".format(storage_name, band)
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
            bands_str = self.storageunitbandtype.bands
            default_bands = self.parameter.default_value.split(',')
            for band in default_bands:
                if band not in bands_str:
                    bands_str += ',' + band

            response = {
                'function_name': self.parameter.function_name,
                'storage_unit_name': "{}".format(self.storageunitbandtype.storage_unit_name),
                'bands': bands_str.split(','),
                'type': self.parameter.parameter_type,
            }
        elif parameter_type == "9":
            response = {
                'function_name': self.parameter.function_name,
                #'start_date': "{}".format(self.timeperiodtype.start_date.strftime('%d-%m-%Y')),
                #'end_date': "{}".format(self.timeperiodtype.end_date.strftime('%d-%m-%Y')),
                # The date is saved in the database as dd-mm-yyyy format and is sended to 
                # the API REST in yyyy-mm-dd format which is the recomended format for the 
                # datacube
                'start_date': "{}".format(self.timeperiodtype.start_date.strftime('%Y-%m-%d')),
                'end_date': "{}".format(self.timeperiodtype.end_date.strftime('%Y-%m-%d')),
                'type': self.parameter.parameter_type,
            }
        elif parameter_type == "12":
            response = {
                'function_name': self.parameter.function_name,
                'value': "{}".format(self.filetype.file_dir()),
                'type': self.parameter.parameter_type,
            }
        elif parameter_type == "13":
            bands_str = self.parameter.default_value
            response = {
                'function_name': self.parameter.function_name,
                'storage_unit_name': self.storageunitnobandtype.storage_unit_name,
                'bands': bands_str.split(','),
                'type': self.parameter.parameter_type,
            }
        elif parameter_type == "14":
            storages_names = self.multistorageunittype.storage_unit_name.split(';')
            storage_bands = self.multistorageunittype.bands.split(';')
            response = {}
            storages = []

            default_storages_bands = self.parameter.default_value.split(';')
            default_storages = {}
            for storage_band_str in default_storages_bands:
                if ':' in storage_band_str:
                    storage_name, bands_str = storage_band_str.split(':')
                    default_storages[storage_name.strip()] = bands_str.split(',')

            for storage_name, bands in zip(storages_names,storage_bands):
                if bands:
                    default_bands = default_storages.get(storage_name.strip(),[])
                    param_bands = bands.split(',')
                    new_bands = list(set(default_bands+param_bands))
                    print("MULTI STORAGE",storage_name,len(storage_name),param_bands,default_bands,new_bands)
                    storages.append(
                        {
                            'name': storage_name,
                            'bands':new_bands
                        }
                    )

            response = {
                'function_name':self.parameter.function_name,
                'storages':storages,
                'type': self.parameter.parameter_type
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

class MultiStorageUnitType(ExecutionParameter):
    storage_unit_name = models.CharField(max_length=500)
    bands = models.CharField(max_length=500)

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


def file_upload_to(instance, filename):
    """File will be uploaded to MEDIA_ROOT/<returned path>."""
    executed_id_str = str(instance.execution.id)
    file_path = os.path.join('downloads',executed_id_str,filename)
    return file_path

class FileType(ExecutionParameter):
    file = models.FileField(
        upload_to=file_upload_to,
        storage=upload_storage,
        validators=[validate_file_extension]
    )

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
    """Each execution can be punctuated after it has finished."""

    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)


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
    parameters = models.TextField(blank=True, null=True)
    trace_error = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)

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
