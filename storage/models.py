# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils import formats
from django.utils import timezone

class StorageUnit(models.Model):

    class Meta:
        permissions = (
            ("can_list_units", "Ver listado de unidades de almacenamiento"),
            ("can_create_units", "Crear unidad de almacenamiento"),
            ("can_view_unit_detail", "Ver detalle de una unidad de almacenamiento"),
            ("can_view_storage_content", "Ver contenido de una unidad de almacenamiento"),
            ("can_download_file", "Descargar un archivo"),
            ("can_view_content_detail", "Ver detalle de un contenido"),
            ("can_download_metadata", "Descargar metadados"),
            ("can_edit_units", "Editar unidad de almacenamiento"),
        )

    alias = models.CharField(max_length=200,unique=True,default='no definido')
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    description_file = models.CharField(max_length=200)
    ingest_file = models.CharField(max_length=200)
    metadata_generation_script = models.CharField(max_length=200)
    metadata = JSONField(blank=True)
    root_dir = models.FilePathField(null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_created_at(self):
        date = self.created_at
        if date:
            date = timezone.localtime(date)
            date = formats.date_format(date,format='DATETIME_FORMAT')
            return date
        return date

    # def __unicode__(self):
    #     return "{} - {}".format(self.id, self.name)

    # def save(self, *args, **kwargs):
    #     if not self.alias:
    #         self.alias = self.name
    #     super(StorageUnit, self).save(*args, **kwargs);
