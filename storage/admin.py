from django.contrib import admin
from storage.models import *

admin.site.register(StorageUnit)
admin.site.register(StorageUnitCDCOL)
admin.site.register(StorageUnitCEOS)
