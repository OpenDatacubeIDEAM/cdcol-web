from algorithm.models import Algorithm
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	versions = serializers.SerializerMethodField()

	class Meta:
		model = Algorithm

	def obtain_version_count(self, obj):
		return obj.obtain_versions.count
