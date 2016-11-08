from rest_framework import serializers
from storage.models import StorageUnit


class StorageUnitSerializer(serializers.ModelSerializer):
	name = serializers.CharField()

	class Meta:
		model = StorageUnit
		fields = ('name', )
