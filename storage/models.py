from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


class StorageUnit(models.Model):
	storage_unit_type = models.CharField(max_length=200)
	processing_level = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	file_description = models.CharField(max_length=200)
	metadata = models.FileField()
	root_dir = models.CharField(max_length=200)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)


class StorageUnitCDCOL(models.Model):
	storage_unit = models.OneToOneField(StorageUnit, on_delete=models.CASCADE)
	detailed_processing_level = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.storage_unit.id, self.storage_unit.name)


class StorageUnitCEOS(models.Model):
	storage_unit = models.OneToOneField(StorageUnit, on_delete=models.CASCADE)
	source_storage_unit = models.ForeignKey(StorageUnit, related_name='source_storage_unit')
	file_feed = models.FileField()

	def __unicode__(self):
		return "{} - {}".format(self.storage_unit.id, self.storage_unit.name)
