from django import forms
from models import UserProfile
from django.contrib.auth.models import Group


class SignupForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ()

	PROFILES_CHOICES = (
		('0', 'Analista',),
		('1', 'Desarrollador',)
	)
	profile_field = forms.ChoiceField(label='Perfil',
	                                  choices=PROFILES_CHOICES,
	                                  widget=forms.RadioSelect())

	def save(self, user):
		"""
		Saving a new user and creating the UserProfile
		:param user: Django' user model
		:return:
		"""
		profile = UserProfile(user=user)
		profile_selected = self.cleaned_data['profile_field']
		if profile_selected == '0':
			profile.is_analyst = True
			analyst_group = Group.objects.get(name='Analyst')
			profile.user.groups.add(analyst_group)
		elif profile_selected == '1':
			profile.is_developer = True
			developer_group = Group.objects.get(name='Developer')
			profile.user.groups.add(developer_group)
		profile.save()
