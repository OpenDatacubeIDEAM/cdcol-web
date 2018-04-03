# -*- coding: utf-8 -*-
from django.contrib import admin
from execution.models import *
from execution.views import cancel_execution
from django.core.exceptions import PermissionDenied


def cancel_execution(self, request, queryset):
	for execution in queryset:
		cancel_execution(execution.id)

cancel_execution.short_description ="Cancelar ejecución"


class ExecutionAdmin(admin.ModelAdmin):
	list_display = (
	'version', 'state', 'created_at', 'results_available', 'results_deleted_at', 'email_sent', 'started_at',
	'finished_at')
	ordering = ('-created_at',)
	list_filter = ('state', 'results_available', 'created_at', 'email_sent', 'started_at', 'finished_at')
	actions = [cancel_execution]

	def save_model(self, request, obj, form, change):
                obj.user = request.user
                raise PermissionDenied

class TaskAdmin(admin.ModelAdmin):
	list_display = ('execution', 'state', 'uuid', 'created_at', 'updated_at', 'start_date', 'end_date', 'state_updated_at')
	ordering = ('-created_at',)
	list_filter = ('state', 'uuid', 'created_at', 'updated_at', 'start_date', 'end_date', 'state_updated_at')
	
class ReviewAdmin(admin.ModelAdmin):
        def save_model(self, request, obj, form, change):
                obj.user = request.user
                raise PermissionDenied


admin.site.register(Execution, ExecutionAdmin)
admin.site.register(ExecutionParameter)
admin.site.register(StringType)
admin.site.register(IntegerType)
admin.site.register(BooleanType)
admin.site.register(AreaType)
admin.site.register(StorageUnitBandType)
admin.site.register(StorageUnitNoBandType)
admin.site.register(TimePeriodType)
admin.site.register(Review, ReviewAdmin)
admin.site.register(DoubleType)
admin.site.register(FileType)
admin.site.register(Task, TaskAdmin)
