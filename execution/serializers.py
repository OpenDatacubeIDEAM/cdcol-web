# -*- coding: utf-8 -*-
from rest_framework import serializers
from execution.models import Execution
from django.db.models import Q


class ExecutionSerializer(serializers.ModelSerializer):
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
		fields = ('id', 'algorithm_name', 'state', 'created_at', 'started_at', 'finished_at', 'current_executions', 'can_rate', 'credits_consumed')

	def get_algorithm_name(self, obj):
		return obj.version.algorithm.name

	def get_state(self, obj):
		return obj.get_state_display()

	def get_current_executions(self, obj):
		return obj.pending_executions().count()

	def get_can_rate(self, obj):
		return obj.can_rate()
