# -*- coding: utf-8 -*-
from django.contrib import admin
from execution.models import *
from execution.views import cancel_execution as cancel
from django.core.exceptions import PermissionDenied



def cancel_execution(self, request, queryset):
	for execution in queryset:
		cancel(request, execution.id)

cancel_execution.short_description = "Cancelar ejecución"

class TaskInline(admin.TabularInline):
	model = Task
	fk_name = 'execution'

class ExecutionAdmin(admin.ModelAdmin):
	list_display = ('id', 'version', 'state', 'executed_by', 'credits_consumed', 'created_at',  'results_available', 'results_deleted_at', 'started_at','finished_at')
	ordering = ('-id',)
	list_filter = (['state'])
	actions = [cancel_execution]
	inlines = [TaskInline]
	def save_model(self, request, obj, form, change):
                obj.user = request.user
                raise PermissionDenied

class TaskAdmin(admin.ModelAdmin):
	list_display = ('id','execution', 'state', 'uuid', 'created_at', 'updated_at', 'start_date', 'end_date', 'state_updated_at')
	ordering = (['-created_at'] )
	list_filter = (['state'])
	
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
