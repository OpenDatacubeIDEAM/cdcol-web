# -*- coding: utf-8 -*-

from django import template
from algorithm.models import Algorithm
from algorithm.models import Version
from storage.models import StorageUnit


register = template.Library()


@register.filter
def get_storage_unit(value):
    """Returns the alias of a storage unit from a parameter

    This filter is used in execution_detail.html
    """
    if "," not in value:
        alias = StorageUnit.objects.get(name=value).alias
    else:
        unit_and_bands=value.split(",", 1)
        alias = "{} ({})".format(StorageUnit.objects.get(name=unit_and_bands[0]).alias, unit_and_bands[1])

    return alias