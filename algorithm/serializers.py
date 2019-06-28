# -*- coding: utf-8 -*-

from django.utils import formats
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
    created_at = serializers.SerializerMethodField()

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

    def get_created_at(self,obj):
        date = obj.created_at 
        date = formats.date_format(
            date, format="DATETIME_FORMAT"
        ) if date else '---'
        return date


class VersionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    algorithm = AlgorithmSerializer()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Version
        fields = (
            'id',
            'name', 
            'number', 
            'algorithm',
            'publishing_state', 
            'created_at'
        )

        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)

    def get_created_at(self,obj):
        return obj.get_created_at()
