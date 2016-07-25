from django import forms
from models import UserProfile


class SignupForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('mobile_number',)

	def save(self, user):
		profile = UserProfile(user=user)
		profile.mobile_number = self.cleaned_data['mobile_number']
		profile.save()
