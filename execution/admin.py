# -*- coding: utf-8 -*-

from django.contrib import admin

from execution.models import Task
from execution.models import Execution
from execution.models import FileConvertionTask


admin.site.register(Task)
admin.site.register(Execution)
admin.site.register(FileConvertionTask)
