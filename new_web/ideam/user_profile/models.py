# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    WAITING_APPROBATION_STATE = '1'
    APPROVED_STATE = '2'
    DENIED_STATED = '3'

    APPROBATION_STATUS = (
        (WAITING_APPROBATION_STATE, "POR APROBACIÓN"),
        (APPROVED_STATE, "APROBADO"),
        (DENIED_STATED, "RECHAZADO"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    usage = models.TextField()
    status = models.CharField(max_length=2, choices=APPROBATION_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    credits_approved = models.IntegerField(default=8, blank=True, null=True)

    def get_groups(self):
        """Result user associated groups."""
        
        user_groups = self.user.groups.values_list('name', flat=True)
        app_groups = []
        if 'DataAdmin' in user_groups:
            app_groups.append('Administrador de Datos')
        if 'Developer' in user_groups:
            app_groups.append('Desarrollador')
        if 'Analyst' in user_groups:
            app_groups.append('Analista')
        
        return app_groups

    def is_data_admin(self):
        return self.user.groups.filter(name='DataAdmin').exists()

    def get_executions(self):
        self.user.execution_set.all()

    # def self(self):
    #     return self

    # def __unicode__(self):
    #     data = (self.id, self.user, self.institution)
    #     return "{} - {} - {}" % data

    # class Meta:
    #     permissions = (
    #         ("can_view_quick_guide_developer", "Puede ver guia rápida de desarrolladores"),
    #         ("can_view_quick_guide_analyst", "Puede ver guia rápida de analista"),
    #     )
