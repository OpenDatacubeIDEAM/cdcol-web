from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from storage.models import StorageUnit


class Topic(models.Model):
	name = models.CharField(max_length=200)
	enabled = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)


class Algorithm(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	source_storage_units = models.ManyToManyField(StorageUnit, through='AlgorithmStorageUnit')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='algorithm_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.id, self.name)

	def obtain_versions(self):
		return Version.objects.filter(algorithm_id=self.id)

	def last_version(self):
		return Version.objects.filter(algorithm_id=self.id).last()


class AlgorithmStorageUnit(models.Model):
	algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='source_algorithm')
	storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, related_name='source_storage_unit')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {}".format(self.algorithm.name, self.storage_unit.name)


class Version(models.Model):
	algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
	description = models.TextField()
	number = models.CharField(max_length=200)
	source_code = models.CharField(max_length=200)
	publishing_state = models.CharField(max_length=200)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='version_author')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {} {}".format(self.id, self.algorithm.name, self.number)

	def new_minor_version(self):
		current_version = self.algorithm.last_version().number
		current_major_version = int(current_version.split('.')[0])
		current_minor_version = int(current_version.split('.')[1])
		return "{}.{}".format(current_major_version, current_minor_version + 1)

	def new_major_version(self):
		current_version = self.algorithm.last_version().number
		current_major_version = int(current_version.split('.')[0])
		return "{}.{}".format(current_major_version + 1, 0)

