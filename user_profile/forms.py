from django import forms
from models import UserProfile
from django.contrib.auth.models import Group


class SignupForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('is_analyst', 'is_developer')

	def save(self, user):
		"""
		Saving a new user and creating the UserProfile
		:param user: Django' user model
		:return:
		"""
		profile = UserProfile(user=user)
		print self.cleaned_data
		profile.is_analyst = self.cleaned_data['is_analyst']
		profile.is_developer = self.cleaned_data['is_developer']
		if profile.is_analyst:
			analyst_group = Group.objects.get(name='Analyst')
			profile.user.groups.add(analyst_group)
		if profile.is_developer:
			developer_group = Group.objects.get(name='Developer')
			profile.user.groups.add(developer_group)
		profile.save()
