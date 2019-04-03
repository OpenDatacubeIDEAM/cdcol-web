# -*- coding: utf-8 -*-

from django.db import models


class Yaml(models.Model):

    class Meta:
        permissions = (
            ("can_list_yaml_templates", "Ver listado de plantillas de archivos YML"),
            ("can_download_yaml_template", "Descargar plantilla de archivo YML"),
        )

    DESCRIPTION_TYPE = '1'
    INGEST_TYPE = '2'
    TYPES = (
        (DESCRIPTION_TYPE, "DESCRIPCIÓN"),
        (INGEST_TYPE, "INGESTA"),
    )

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='template/yaml/')
    ttype = models.CharField(max_length=2, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __unicode__(self):
    #     return "{} - {} - {}".format(
    #         self.name, self.get_type_display(), self.created_at
    #     )


class Ingest(models.Model):

    class Meta:
        permissions = (
            ("can_list_ingest_templates", "Ver listado de scritps de generación de metadatos"),
            ("can_download_metadata_script", "Descargar scripts de generación de metadatos (.py)"),
        )

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='template/ingest/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __unicode__(self):
    #     return "{}".format(self.name)

