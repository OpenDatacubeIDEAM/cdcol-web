# -*- coding: utf-8 -*-
from rest_framework import serializers
from execution.models import Execution


class ExecutionSerializer(serializers.ModelSerializer):
	algorithm_name = serializers.SerializerMethodField()
	state = serializers.SerializerMethodField()
	created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
	started_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
	finished_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

	class Meta:
		model = Execution
		fields = ('id', 'algorithm_name', 'state', 'created_at', 'started_at', 'finished_at')

	def get_algorithm_name(self, obj):
		return obj.version.algorithm.name

	def get_state(self, obj):
		return obj.get_state_display()
