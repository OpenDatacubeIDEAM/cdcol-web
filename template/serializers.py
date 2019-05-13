# -*- coding: utf-8 -*-

from rest_framework import serializers
from template.models import Yaml
from template.models import Ingest


class YamlSerializer(serializers.ModelSerializer):
    
    type = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Yaml
        fields = ('id', 'name', 'type', 'created_at','file')

        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)

    def get_ttype(self, obj):
        """Returns the display string assigned to choice fields."""
        return obj.get_ttype_display()


class IngestSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Yaml
        fields = ('id', 'name', 'created_at','file')