from django import template
from algorithm.models import Algorithm, Version
from storage.models import StorageUnit
# registering a new filter
register = template.Library()


@register.filter(name="get_algorithms")
def get_algorithms(value):
	"""Returns all the algorithms belonging to a certain topic"""
	return Algorithm.objects.filter(topic=value)

register.filter('get_algorithms', get_algorithms)


@register.filter(name="last_version_id")
def last_version_id(algorithm):
	"""Returns last version id"""
	versions = Version.objects.filter(algorithm_id=algorithm.id)
	return versions.last().id if versions else 0

register.filter('last_version_id', last_version_id)

@register.filter(name="get_storage_unit")
def get_storage_unit(value):
	"""Returns the alias of a storage unit from a parameter"""
	if "," not in value:
		alias = StorageUnit.objects.get(name="value").alias
	else:
		unit_and_bands=value.split(",", 1)
		alias = StorageUnit.objects.get(name=unit_and_bands[0]).alias

	return alias

register.filter('get_storage_unit', get_storage_unit)