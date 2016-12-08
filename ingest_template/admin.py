# -*- coding: utf-8 -*-
from django.contrib import admin
from ingest_template.models import *


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')
	ordering = ('-created_at',)
	search_fields = ('name', 'created_at', )
	list_filter = ('created_at',)

	def get_readonly_fields(self, request, obj=None):
		"""
		overriding the readonly_fields method
		"""
		if request.user.groups.filter(name='DataAdmin').exists():
			self.readonly_fields = self.dynamic_readonly_fields()
		return super(EventAdmin, self).get_readonly_fields(request, obj)

	def dynamic_readonly_fields(self):
		"""
		setting the readonly_fields
		based on http://stackoverflow.com/a/31787817/4808337 answer
		"""
		readonly_fields = ('id', 'name', 'file', 'created_at')
		return readonly_fields


admin.site.register(IngestTemplate, EventAdmin)
