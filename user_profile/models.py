# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	WAITING_APPROBATION_STATE = '1'
	APPROVED_STATE = '2'
	DENIED_STATED = '3'
	# All the states
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

	def __unicode__(self):
		return "{} - {} - {}".format(self.id, self.user, self.institution)
	class Meta:
		permissions = (
			("can_view_quick_guide_developer", "Puede ver guia rápida de desarrolladores"),
			("can_view_quick_guide_analyst", "Puede ver guia rápida de analista"),
		)
