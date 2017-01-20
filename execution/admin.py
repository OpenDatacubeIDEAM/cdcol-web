# -*- coding: utf-8 -*-
from django.contrib import admin
from execution.models import *


class ExecutionAdmin(admin.ModelAdmin):
	list_display = (
	'version', 'state', 'created_at', 'results_available', 'results_deleted_at', 'email_sent', 'started_at',
	'finished_at')
	ordering = ('-created_at',)
	list_filter = ('state', 'results_available', 'created_at', 'email_sent', 'started_at', 'finished_at')

class TaskAdmin(admin.ModelAdmin):
	list_display = ('execution', 'state', 'uuid', 'created_at', 'updated_at', 'start_date', 'end_date', 'state_updated_at')
	ordering = ('-created_at',)
	list_filter = ('state', 'uuid', 'created_at', 'updated_at', 'start_date', 'end_date', 'state_updated_at')


admin.site.register(Execution, ExecutionAdmin)
admin.site.register(ExecutionParameter)
admin.site.register(StringType)
admin.site.register(IntegerType)
admin.site.register(BooleanType)
admin.site.register(AreaType)
admin.site.register(StorageUnitBandType)
admin.site.register(StorageUnitNoBandType)
admin.site.register(TimePeriodType)
admin.site.register(Review)
admin.site.register(DoubleType)
admin.site.register(FileType)
admin.site.register(Task, TaskAdmin)
