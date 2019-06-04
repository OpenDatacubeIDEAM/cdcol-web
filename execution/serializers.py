# -*- coding: utf-8 -*-

from rest_framework import serializers
from execution.models import Execution
from algorithm.serializers import VersionSerializer

from datetime import timedelta


class ExecutionSerializer(serializers.ModelSerializer):

    AIRFLOW_STATES = {
        'running': "EN EJECUCIÓN",
        'success': "FINALIZADA",
        'failed': "CON FALLO"
    }

    version = VersionSerializer()
    state = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    started_at = serializers.SerializerMethodField()
    finished_at = serializers.SerializerMethodField()
    current_executions = serializers.SerializerMethodField()
    can_rate = serializers.SerializerMethodField()
    credits_consumed = serializers.IntegerField()

    class Meta:
        model = Execution
        fields = [
            'id', 'state','version', 'created_at', 
            'started_at', 'finished_at', 'current_executions', 
            'can_rate', 'credits_consumed'
        ]

    def get_algorithm_name(self, obj):
        return obj.version.algorithm.name

    def get_state(self, obj):
        dag_state = obj.get_state_display()
        dag_run = obj.get_dag_run()
        if dag_run:
            dag_state = self.AIRFLOW_STATES.get(dag_run.state)

        return dag_state

    def get_created_at(self,obj):
        return obj.get_created_at()

    def get_started_at(self,obj):
        return obj.get_started_at() 

    def get_finished_at(self,obj):
        return obj.get_finished_at()

    def get_current_executions(self, obj):
        return obj.pending_executions().count()

    def get_can_rate(self, obj):
        return obj.can_rate()


class Task(object):
    def __init__(self, **kwargs):
        fields = (
            'id', 'state', 'log_url', 'log_filepath','execution_date',
            'start_date','end_date', 'duration', 'log_content'
        )
        for field in fields:
            setattr(self, field, kwargs.get(field, None))


class TaskSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    state = serializers.CharField(max_length=256)
    log_url = serializers.URLField(max_length=900, min_length=None, allow_blank=False)
    log_filepath = serializers.CharField(max_length=900)
    log_content = serializers.CharField(allow_blank=True)
    execution_date = serializers.DateTimeField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    duration = serializers.FloatField()

    def create(self, validated_data):
        return Task(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
