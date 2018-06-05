# -*- coding:utf-8 -*-
from django import template
from execution.models import Execution
from user_profile.models import UserProfile
# registering a new filter
register = template.Library()


@register.filter('has_group')
def has_group(user, group_name):
	"""Verify if user is in group"""
	groups = user.groups.all().values_list('name', flat=True)
	return True if group_name in groups else False

@register.inclusion_tag('public/menu_executions.html')
def get_execution(user):
	#executions = Execution.objects.filter(state__in=[Execution.EXECUTING_STATE, Execution.ENQUEUED_STATE], cr)
	executions = Execution.objects.filter(executed_by=user)
	used_credits = user.id
	available_credits = UserProfile.objects.get(user=user).credits_approved
	return {'executions': executions, 'used_credits': used_credits, 'available_credits': available_credits}