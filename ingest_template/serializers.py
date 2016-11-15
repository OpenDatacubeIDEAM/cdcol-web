from rest_framework import serializers
from ingest_template.models import IngestTemplate


class IngestScriptSerializer(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
	updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

	class Meta:
		model = IngestTemplate
		fields = ('id', 'name', 'created_at', 'updated_at')
