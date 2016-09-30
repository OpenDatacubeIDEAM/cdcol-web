from django import template
from algorithm.models import Algorithm

# registering a new filter
register = template.Library()


@register.filter(name="get_algorithms")
def get_algorithms(value):
	"""Returns all the algorithms belonging to a certain topic"""
	return Algorithm.objects.filter(topic=value)

register.filter('get_algorithms', get_algorithms)
