# -*- coding: utf-8 -*-
from django.contrib import admin
from template.models import *


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', 'created_at')
	ordering = ('-created_at',)
	search_fields = ['name', 'type']
	list_filter = ('type', 'created_at')

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
		readonly_fields = ('id', 'name', 'type', 'file', 'created_at', 'updated_at')
		return readonly_fields


admin.site.register(YamlTemplate, EventAdmin)
