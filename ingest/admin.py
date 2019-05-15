# -*- coding: utf-8 -*-

from django.contrib import admin
from ingest.models import IngestTask


class EventAdmin(admin.ModelAdmin):
    list_display = ('storage_unit', 'state', 'created_by', 'created_at')
    ordering = ('-created_at',)
    search_fields = ['storage_unit', 'state', 'created_by']
    list_filter = ('state',)

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
        readonly_fields = (
            'storage_unit', 'state', 'comments', 
            'error_messages', 'logs', 'start_execution_date', 
            'end_execution_date','created_by', 'created_at', 'updated_at'
        )
        return readonly_fields


admin.site.register(IngestTask, EventAdmin)
