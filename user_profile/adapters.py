from allauth.account.adapter import DefaultAccountAdapter
from user_profile.models import UserProfile
from django.contrib.auth import logout


class MyAccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		user_profile = UserProfile.objects.get(user=request.user)
		print user_profile.get_status_display()
		print user_profile.status
		print UserProfile.APPROBATION_STATUS
		if int(user_profile.status) == int(UserProfile.APPROVED_STATE):
			return "/home/"
		else:
			logout(request)
			return "/profile/pending/"
