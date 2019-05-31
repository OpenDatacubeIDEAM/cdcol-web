# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from execution.models import Task
from execution.models import Review
from execution.models import Execution
from execution.models import ExecutionParameter
from execution.models import FileConvertionTask
from execution.models import StringType
from execution.models import IntegerType
from execution.models import DoubleType
from execution.models import BooleanType
from execution.models import AreaType
from execution.models import StorageUnitBandType
from execution.models import StorageUnitNoBandType
from execution.models import TimePeriodType
from execution.models import validate_file_extension
from execution.models import get_upload_to
from execution.models import FileType
from execution.models import MultipleChoiceListType
from execution.views import ExecutionCancelView


class TaskInline(admin.TabularInline):
    model = Task
    fk_name = 'execution'


class ExecutionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'version', 'state', 'executed_by', 
        'credits_consumed', 'created_at',  
        'results_available', 'results_deleted_at', 
        'started_at','finished_at'
    )
    ordering = ('-id',)
    list_filter = (['state'])
    actions = ['cancel_execution']
    inlines = [TaskInline]

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     raise PermissionDenied

    def cancel_execution(self, request, queryset):
        for execution in queryset:
            response = ExecutionCancelView.as_view()(request, pk=execution.id)

            if not isinstance(response,dict):
                if response.status_code == 200:
                    self.message_user(
                        request,'Ejecución %s cancelada con éxito.' % execution.id
                    )
                else:
                    self.message_user(
                        request,'La Ejecución %s no pudo ser cancelada.' % execution.id, 
                        level=messages.ERROR
                    )
                    self.message_user(request,response.text,level=messages.ERROR)
            else:
                self.message_user(
                    request,
                    'Error e interntar conectarse con la API REST.',
                    level=messages.ERROR)
                self.message_user(
                    request,
                    str(response.get('exception')),
                    level=messages.ERROR
                )


    cancel_execution.short_description = "Cancelar ejecución"


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id','execution', 'state', 'uuid', 
        'created_at', 'updated_at', 'start_date', 
        'end_date', 'state_updated_at'
    )
    ordering = (['-created_at'] )
    list_filter = (['state'])
    

class ReviewAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        raise PermissionDenied


admin.site.register(ExecutionParameter)
admin.site.register(FileConvertionTask)
admin.site.register(StringType)
admin.site.register(IntegerType)
admin.site.register(DoubleType)
admin.site.register(BooleanType)
admin.site.register(AreaType)
admin.site.register(StorageUnitBandType)
admin.site.register(StorageUnitNoBandType)
admin.site.register(TimePeriodType)
admin.site.register(FileType)
admin.site.register(MultipleChoiceListType)
admin.site.register(Task,TaskAdmin)
admin.site.register(Execution,ExecutionAdmin)
admin.site.register(Review, ReviewAdmin)