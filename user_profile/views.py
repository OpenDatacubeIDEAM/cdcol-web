# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import TemplateView

from user_profile.forms import ProfileForm


class PendingView(TemplateView):
    """This page is rendered when a user is just registered."""
    template_name = 'user_profile/pending.html'


class HomeView(TemplateView):
    """Render the user home page."""
    template_name = 'user_profile/home.html'


class UpdateView(TemplateView):
    """Update user and profile models data."""
    
    def get(self,request,*args,**kwargs):
        initial = {
            'email': request.user.email,
            'name': request.user.first_name,
            'last_name': request.user.last_name,
            'institution': request.user.profile.institution,
            'phone': request.user.profile.phone
        }
        form = ProfileForm(initial=initial)
        context = {'user_form':form}
        return render(request,'user_profile/update.html',context)

    def post(self,request,*args,**kwargs):

        form = ProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            institution = form.cleaned_data['institution']
            phone = form.cleaned_data['phone']
            # updating User model
            request.user.first_name = name
            request.user.last_name = last_name
            request.user.save()
            # updating UserProfile model
            request.user.profile.institution = institution
            request.user.profile.phone = phone
            request.user.profile.save()

        context = {'user_form':form}
        return render(request,'user_profile/update.html',context)