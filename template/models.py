# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


"""
Used to upload file outside the proyect base directory
"""
upload_storage = FileSystemStorage(location=settings.MEDIA_ROOT)


class Yaml(models.Model):
    """
    Product Definition (DESCRIPTION_TYPE)

        Product = Satelites

        "Product description document defines some of the metadata common to all 
        the datasets belonging to the products. It also describes the measurements 
        that product has and some of the properties of the measurements."

        Example:

        name: dsm1sv10
        description: DSM 1sec Version 1.0
        metadata_type: eo
        ...

        Reference: https://datacube-core.readthedocs.io/en/latest/ops/product.html


    Ingestion Type (INGEST_TYPE)

        "An ingestion config is a document which defines the way data should be 
        prepared for high performance access. This can include slicing the data 
        into regular chunks, reprojecting into to the desired projection and 
        compressing the data."

        An Ingestion Config is written in YAML and contains the following:

        * Source Product name - source_type
        * Output Product name - output_type
        ....

        Reference: https://datacube-core.readthedocs.io/en/latest/ops/ingest.html

    """

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
    file = models.FileField(upload_to='template/yaml/',storage=upload_storage)
    type = models.CharField(max_length=2, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __unicode__(self):
    #     return "{} - {} - {}".format(
    #         self.name, self.get_type_display(), self.created_at
    #     )


class Ingest(models.Model):
    """
    Dataset Preparation Scripts for Ingest Data

        "Some data you may want to load into your Data Cube will come pre-packaged 
        with a dataset-description document and is ready to be indexed/loaded immediately.

        In many other cases the data you want to load into your Data Cube will not have these 
        description documents. Before loading them will need to generate them, using a tool 
        which understands the format the dataset is in. Several of these tools are provided 
        in utils/ in the source repository."

        This files are python scripts .py

        Reference: https://datacube-core.readthedocs.io/en/latest/ops/prepare_scripts.html
    """

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

