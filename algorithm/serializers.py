# -*- coding: utf-8 -*-

from rest_framework import serializers
from algorithm.models import Algorithm
from algorithm.models import Topic
from algorithm.models import Version


class TopicSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Topic
        fields = (
            'id', 
            'name', 
            'enabled', 
            'created_at'
        )
        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)


class AlgorithmSerializer(serializers.ModelSerializer):

    topic = TopicSerializer()
    version_count = serializers.ReadOnlyField()
    last_version_status = serializers.ReadOnlyField()
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Algorithm
        fields = (
            'id', 
            'name', 
            'topic',
            'version_count', 
            'last_version_status', 
            'created_at'
        )
        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)


class VersionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    algorithm = AlgorithmSerializer()

    class Meta:
        model = Version
        fields = (
            'id', 
            'number', 
            'algorithm',
            'publishing_state', 
            'created_at'
        )

        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)