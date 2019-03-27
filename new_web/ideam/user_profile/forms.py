# -*- coding: utf-8 -*-

from django import forms
from user_profile.models import Profile


class SignupForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, label='Nombres', required=True)
    last_name = forms.CharField(max_length=30, label='Apellidos', required=True)
    institution = forms.CharField(max_length=200, label='Institución', required=True)
    phone = forms.CharField(max_length=200, label='Teléfono Institucional', required=True)
    usage = forms.CharField(widget=forms.Textarea(attrs={
            'rows': 3,'class': 'form-control','placeholder': '¿Para qué desea utilizar CDCOL?'
            }), required=True
    )

    class Meta:
        model = Profile
        fields = ('institution', 'phone', 'usage', )

    def save(self, user):
        """
        Saving a new user and creating the UserProfile
        :param user: Django' user model
        :return:
        """
        # Saving the User model
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Saving the UserProfile model
        profile = Profile(user=user)
        profile.institution = self.cleaned_data['institution']
        profile.phone = self.cleaned_data['phone']
        profile.usage = self.cleaned_data['usage']
        profile.status = Profile.WAITING_APPROBATION_STATE
        profile.save()
