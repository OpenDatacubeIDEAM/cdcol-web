# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from user_profile.models import UserProfile
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
import re


class MyAccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		user_profile = UserProfile.objects.get(user=request.user)
		if int(user_profile.status) == int(UserProfile.APPROVED_STATE):
			return "/home/"
		else:
			logout(request)
			return "/profile/pending/"

	def clean_password(self, password):
		if re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$', password):
			return password
		else:
			raise ValidationError("La contraseña debe tener mínimo 8 caracteres, contener minúsculas y mayúsculas.")
