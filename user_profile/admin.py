# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from user_profile.models import UserProfile
from allauth.account.utils import send_email_confirmation


def assign_user_to_group(modeladmin, queryset, group_name, request):
    """
    Approves users
    :param queryset: List of the users to be approved
    :param group: Group to be assigned
    :param request:
    :return:
    """
    group = Group.objects.get(name=group_name)
    if group:
        for user_profile in queryset:
            user_profile.status = UserProfile.APPROVED_STATE
            user_profile.save()
            # sending the confirmation email
            send_email_confirmation(request, user_profile.user, signup=True)
            # setting the group
            group.user_set.add(user_profile.user)
            modeladmin.message_user(
                request,
                'El usuario %s fue agregado al grupo %s con éxito.' % (user_profile.user.first_name,group.name)
            )
    else:
        self.message_user(
            request,'El grupo %s no existe.' % group_name, 
            level=messages.ERROR
        )


def set_developer_role(modeladmin, request, queryset):
    """
    Custom action to set the developer role to all the users selected
    """
    assign_user_to_group(modeladmin, queryset, 'Developer', request)


def set_analyst_role(modeladmin, request, queryset):
    """
    Custom action to set the analyst role to all the users selected
    """
    assign_user_to_group(modeladmin, queryset, 'Analyst', request)


def set_data_admin_role(modeladmin, request, queryset):
    """
    Custom action to set the data admin role to all the users selected
    """
    assign_user_to_group(modeladmin, queryset, 'DataAdmin', request)

def set_workflow_reviewer_role(modeladmin, request, queryset):
    """
    Custom action to set the data admin role to all the users selected
    """
    assign_user_to_group(modeladmin, queryset, 'WorkflowReviewer', request)

def decline_users(modeladmin, request, queryset):
    """
    Custom action to delete all the users selected
    """
    for user_profile in queryset:
        user_profile.user.delete()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'user_email', 'credits_approved', 
        'institution', 'phone', 'status', 'created_at',
        'user_groups'
    )
    ordering = ('-created_at',)
    search_fields = ('user__email', 'institution', 'status')
    list_filter = ('status', 'created_at')
    actions = [
        set_developer_role, 
        set_analyst_role, 
        set_data_admin_role,
        set_workflow_reviewer_role, 
        decline_users,
    ]

    def full_name(self, user_profile):
        """
        Return user full name.
        """
        first_name = user_profile.user.first_name
        last_name = user_profile.user.last_name
        return "{} {}".format(first_name,last_name)

    def user_email(self, user_profile):
        """
        Return user email.
        """
        return user_profile.user.email

    def get_readonly_fields(self, request, obj=None):
        """
        overriding the readonly_fields method
        """
        if request.user.groups.filter(name='DataAdmin').exists():
            self.readonly_fields = self.dynamic_readonly_fields()
        return super(UserProfileAdmin, self).get_readonly_fields(request, obj)

    def user_groups(self, user_profile):
        """
        Return user groups string separed by comas.
        """
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
        readonly_fields = (
            'user', 'institution', 'phone', 
            'usage', 'credits_approved', 
            'status', 'created_at', 
            'updated_at', 'user_groups'
        )
        return readonly_fields

    full_name.short_description = 'Full Name'
    user_email.short_description = 'User Email'


decline_users.short_description = "Rechazar usuario"
set_developer_role.short_description = "Aprobar y asignar permiso de Desarrollador"
set_analyst_role.short_description = "Aprobar y asignar permiso de Analista"
set_data_admin_role.short_description = "Aprobar y signar permiso de Administrador de Datos"
set_workflow_reviewer_role.short_description = "Aprobar y asignar premiso de Analista de Workflows"

admin.site.register(UserProfile, UserProfileAdmin)
