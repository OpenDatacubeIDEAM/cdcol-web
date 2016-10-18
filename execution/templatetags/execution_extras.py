from django import template
from algorithm.models import Algorithm, Version

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
