from rest_framework import serializers
from template.models import YamlTemplate


class YamlSerializer(serializers.ModelSerializer):
	# name = serializers.CharField()
	type = serializers.SerializerMethodField()
	created_at = serializers.DateTimeField(format="%d-%m-%Y")

	class Meta:
		model = YamlTemplate
		fields = ('id', 'name', 'type', 'created_at')

	def get_type(self, obj):
		return obj.get_type_display()
