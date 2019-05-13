 # -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.contrib import messages

from user_profile.models import UserProfile


class IndexView(TemplateView):

    def get(self,request,*args,**kwargs):

        # The following verifications must be given 
        # in the order presented here.
        if request.user.is_anonymous:
            template_name = 'index/index.html'
            return render(request,template_name)
        
        if request.user.is_superuser:
            return redirect('admin:index')

        if request.user.profile.status in UserProfile.WAITING_APPROBATION_STATE:
            # When a new user is registered allauth authenticated them
            # automatically. To avoid this we logout the user and 
            # delete the messages that allouth place in messages when it 
            # authenticates the user.  
            logout(request)
            return redirect('profile:pending')

        if request.user.is_authenticated:
            return redirect('profile:home')



        


