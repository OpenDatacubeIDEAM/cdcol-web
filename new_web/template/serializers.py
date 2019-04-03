# -*- coding: utf-8 -*-

from rest_framework import serializers
from template.models import Yaml


class YamlSerializer(serializers.ModelSerializer):
    
    ttype = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Yaml
        fields = ('id', 'name', 'type', 'created_at')

        # django-rest-framework-datatables
        datatables_always_serialize = ('id',)

    def get_ttype(self, obj):
        return obj.get_type_display()