# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class YamlTemplate(models.Model):
	DESCRIPTION_TYPE = '1'
	INGEST_TYPE = '2'
	TYPES = (
		(DESCRIPTION_TYPE, "DESCRIPCIÓN"),
		(INGEST_TYPE, "INGESTA"),
	)
	name = models.CharField(max_length=200)
	file = models.FileField()
	type = models.CharField(max_length=2, choices=TYPES)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{} - {} - {}".format(self.name, self.get_type_display(), self.created_at)
