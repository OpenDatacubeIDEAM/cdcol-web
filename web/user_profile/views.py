# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_profile.models import UserProfile
from user_profile.forms import UserProfileForm


def pending(request):
	return render(request, 'profile/pending.html')


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	user_profile = UserProfile.objects.get(user=current_user)
	if request.method == 'POST':
		# getting the form
		user_form = UserProfileForm(request.POST)
		# checking if the form is valid
		if user_form.is_valid():
			name = user_form.cleaned_data['name']
			last_name = user_form.cleaned_data['last_name']
			institution = user_form.cleaned_data['institution']
			phone = user_form.cleaned_data['phone']
			# updating User model
			current_user.first_name = name
			current_user.last_name = last_name
			current_user.save()
			# updating UserProfile model
			user_profile.institution = institution
			user_profile.phone = phone
			user_profile.save()
		else:
			user_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		user_form = UserProfileForm(initial={
			'email': current_user.email,
			'name': current_user.first_name,
			'last_name': current_user.last_name,
			'institution': user_profile.institution,
			'phone': user_profile.phone})
	context = {'user_form': user_form}
	return render(request, 'profile/index.html', context)
