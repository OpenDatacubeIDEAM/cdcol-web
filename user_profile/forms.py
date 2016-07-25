from django import forms
from models import UserProfile


class SignupForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('is_analyst', 'is_developer')

	def save(self, user):
		profile = UserProfile(user=user)
		profile.is_analyst = self.cleaned_data['is_analyst']
		profile.is_developer = self.cleaned_data['is_developer']
		profile.save()
