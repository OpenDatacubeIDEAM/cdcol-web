# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


def get_upload_to(new_ingest_template, filename):
	return "uploads/ingest_template/file/{}".format(filename)


class IngestTemplate(models.Model):
	name = models.CharField(max_length=200)
	file = models.FileField(upload_to=get_upload_to)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{}".format(self.name)
