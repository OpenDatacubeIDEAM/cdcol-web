# -*- coding: utf-8 -*-

from rest_framework import serializers
from algorithm.models import Algorithm


class AlgorithmSerializer(serializers.ModelSerializer):
    # topic = serializers.SerializerMethodField()
    version_count = serializers.ReadOnlyField()
    last_version_status = serializers.ReadOnlyField()
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Algorithm
        fields = (
            'id', 'name', 
            'version_count', 'last_version_status', 
            'created_at'
        )
        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)

    # def get_topic(self, obj):
    #     return obj.topic.name
