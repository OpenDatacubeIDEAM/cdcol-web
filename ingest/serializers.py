# -*- coding: utf-8 -*-

from rest_framework import serializers
from ingest.models import IngestTask


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class StorageUnitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class TaskSerializer(serializers.ModelSerializer):
    storage_unit = StorageUnitSerializer()
    created_by = UserSerializer()
    state = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = IngestTask
        fields = ('id', 'storage_unit', 'state', 'created_at', 'created_by')

    def get_state(self, obj):
        return obj.get_state_display()

    def get_created_at(self,obj):
        return obj.get_created_at()
