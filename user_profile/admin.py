# -*- coding: utf-8 -*-
from django.contrib import admin
from user_profile.models import *
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import Group


def assign_user_to_group(queryset, group, request):
	"""
	Approves users
	:param queryset: List of the users to be approved
	:param group: Group to be assigned
	:param request:
	:return:
	"""
	group = Group.objects.get(name=group)
	if group:
		for user_profile in queryset:
			user_profile.status = UserProfile.APPROVED_STATE
			user_profile.save()
			print '1'
			# sending the confirmation email
			print '2'
			send_email_confirmation(request, user_profile.user, signup=True)
			# setting the group
			print '3'
			group.user_set.add(user_profile.user)
	else:
		print "Could not find the {} group.".format(group)


def set_developer_role(modeladmin, request, queryset):
	"""
	Custom action to set the developer role to all the users selected
	"""
	assign_user_to_group(queryset, 'Developer', request)


def set_analyst_role(modeladmin, request, queryset):
	"""
	Custom action to set the analyst role to all the users selected
	"""
	assign_user_to_group(queryset, 'Analyst', request)


def set_data_admin_role(modeladmin, request, queryset):
	"""
	Custom action to set the data admin role to all the users selected
	"""
	assign_user_to_group(queryset, 'DataAdmin', request)


def decline_users(modeladmin, request, queryset):
	"""
	Custom action to delete all the users selected
	"""
	for user_profile in queryset:
		user_profile.user.delete()


class EventAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'user_email', 'credits_approved', 'institution', 'phone', 'status', 'created_at')
	ordering = ('-created_at',)
	search_fields = ('user__email', 'institution', 'status')
	list_filter = ('status', 'created_at')
	actions = [set_developer_role, set_analyst_role, set_data_admin_role, decline_users]

	def full_name(self, user_profile):
		return "{} {}".format(user_profile.user.first_name.encode('utf-8'), user_profile.user.last_name.encode('utf-8'))

	def user_email(self, user_profile):
		return user_profile.user.email

	def get_readonly_fields(self, request, obj=None):
		"""
		overriding the readonly_fields method
		"""
		if request.user.groups.filter(name='DataAdmin').exists():
			self.readonly_fields = self.dynamic_readonly_fields()
		return super(EventAdmin, self).get_readonly_fields(request, obj)

	def user_groups(self, user_profile):
		response = ""
		groups = user_profile.user.groups.all()
		for group in groups:
			response += "{},".format(group.name)
		return response

	def dynamic_readonly_fields(self):
		"""
		setting the readonly_fields
		based on http://stackoverflow.com/a/31787817/4808337 answer
		"""
		readonly_fields = ('user', 'institution', 'phone', 'usage', 'credits_approved', 'status', 'created_at', 'updated_at', 'user_groups')
		return readonly_fields

	full_name.short_description = 'Full Name'
	user_email.short_description = 'User Email'


decline_users.short_description = "Rechazar usuario"
set_developer_role.short_description = "Aprobar y asignar permiso de Desarrollador"
set_analyst_role.short_description = "Aprobar y asignar permiso de Analista"
set_data_admin_role.short_description = "Aprobar y signar permiso de Administrador de Datos"

admin.site.register(UserProfile, EventAdmin)
