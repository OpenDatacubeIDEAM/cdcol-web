from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


class StorageUnit(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	description_file = models.FileField()
	ingest_file = models.FileField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)


class Content(models.Model):
	metadata = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class IngestedContent(Content):
	storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
	path = models.CharField(max_length=200)

	def __unicode__(self):
		return "{} - {}".format(self.storage_unit.name, self.path)
