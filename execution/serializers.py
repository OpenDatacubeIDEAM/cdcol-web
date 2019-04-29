# -*- coding: utf-8 -*-

from rest_framework import serializers
from execution.models import Execution

from airflow.models import DagRun


class ExecutionSerializer(serializers.ModelSerializer):

    AIRFLOW_STATES = {
        'running': Execution.EXECUTING_STATE,
        'success': Execution.COMPLETED_STATE,
        'failed': Execution.ERROR_STATE
    }

    algorithm_name = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    started_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    finished_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    current_executions = serializers.SerializerMethodField()
    can_rate = serializers.SerializerMethodField()
    credits_consumed = serializers.IntegerField()

    class Meta:
        model = Execution
        fields = [
            'id', 'algorithm_name', 'state', 'created_at', 
            'started_at', 'finished_at', 'current_executions', 
            'can_rate', 'credits_consumed'
        ]

    def get_algorithm_name(self, obj):
        return obj.version.algorithm.name

    def get_state(self, obj):
        dag_state = obj.get_state_display()

        if not obj.finished_at:
            dr_list = DagRun.find(dag_id=obj.dag_id)
            if dr_list:
                dag_state = dr_list[-1].state
                dag_state = AIRFLOW_STATES.get(dag_state)

        return dag_state

    def get_current_executions(self, obj):
        return obj.pending_executions().count()

    def get_can_rate(self, obj):
        return obj.can_rate()


class Task(object):
    def __init__(self, **kwargs):
        fields = (
            'id', 'state', 'log_url', 'execution_date',
            'start_date','end_date', 'duration'
        )
        for field in fields:
            setattr(self, field, kwargs.get(field, None))


class TaskSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    state = serializers.CharField(max_length=256)
    log_url = serializers.URLField(max_length=900, min_length=None, allow_blank=False)
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