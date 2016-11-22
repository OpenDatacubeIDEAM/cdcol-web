# -*- coding:utf-8 -*-
from django import template

# registering a new filter
register = template.Library()


@register.filter('has_group')
def has_group(user, group_name):
	"""Verify if user is in group"""
	groups = user.groups.all().values_list('name', flat=True)
	return True if group_name in groups else False
