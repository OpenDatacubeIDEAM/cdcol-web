from django import template
from algorithm.models import Algorithm, Version
from storage.models import StorageUnit
# registering a new filter
register = template.Library()


@register.filter(name="get_algorithms")
def get_algorithms(value):
	"""Returns all the algorithms belonging to a certain topic"""

	#query = 'SELECT * FROM algorithm_algorithm AS alg LEFT JOIN algorithm_version AS ver ON alg.id = ver.id WHERE ( ver.publishing_state=\'2\') AND alg.topic_id={}'.format(str(value.id))
	#return Algorithm.objects.raw(query);
	return 	Algorithm.objects.filter(topic=value, version__publishing_state=Version.PUBLISHED_STATE)

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
		alias = StorageUnit.objects.get(name=value).alias
	else:
		unit_and_bands=value.split(",", 1)
		alias = "{} ({})".format(StorageUnit.objects.get(name=unit_and_bands[0]).alias, unit_and_bands[1])

	return alias

register.filter('get_storage_unit', get_storage_unit)