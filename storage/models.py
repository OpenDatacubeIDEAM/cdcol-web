from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


class StorageUnit(models.Model):
	alias = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField()
	description_file = models.CharField(max_length=200)
	ingest_file = models.CharField(max_length=200)
	metadata_generation_script = models.CharField(max_length=200)
	metadata = JSONField()
	root_dir = models.FilePathField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)

	class Meta:
		permissions = (
			("can_list_units", "Ver listado de unidades de almacenamiento"),
			("can_create_units", "Crear unidad de almacenamiento"),
			("can_view_unit_detail", "Ver detalle de una unidad de almacenamiento"),
			("can_view_storage_content", "Ver contenido de una unidad de almacenamiento"),
			("can_download_file", "Descargar un archivo"),
			("can_view_content_detail", "Ver detalle de un contenido"),
			("can_download_metadata", "Descargar metadados"),
		)
