from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_analyst = models.BooleanField(default=False)
	is_developer = models.BooleanField(default=False)
