# -*- coding: utf-8 -*-

from django.contrib import admin

from execution.models import Task
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


admin.site.register(Task)
admin.site.register(Execution)
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