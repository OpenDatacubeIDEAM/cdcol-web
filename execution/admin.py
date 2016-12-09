from django.contrib import admin
from execution.models import *

admin.site.register(Execution)
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
admin.site.register(Task)
