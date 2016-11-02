from __future__ import unicode_literals

from django.db import models


class YamlTemplate(models.Model):
	name = models.CharField(max_length=200)
	file = models.FileField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
