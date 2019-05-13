# -*- coding: utf-8 -*-

from django import forms
from user_profile.models import UserProfile


class SignupForm(forms.ModelForm):
    """User registration, this is used for 'allouth' app."""

    first_name = forms.CharField(max_length=30, label='Nombres', required=True)
    last_name = forms.CharField(max_length=30, label='Apellidos', required=True)
    institution = forms.CharField(max_length=200, label='Institución', required=True)
    phone = forms.CharField(max_length=200, label='Teléfono Institucional', required=True)
    usage = forms.CharField(widget=forms.Textarea(attrs={
            'rows': 3,'class': 'form-control','placeholder': '¿Para qué desea utilizar CDCOL?'
            }), required=True
    )

    class Meta:
        model = UserProfile
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
        profile = UserProfile(user=user)
        profile.institution = self.cleaned_data['institution']
        profile.phone = self.cleaned_data['phone']
        profile.usage = self.cleaned_data['usage']
        profile.status = UserProfile.WAITING_APPROBATION_STATE
        profile.save()


class ProfileForm(forms.Form):
    """User profile personal data update."""
    
    email = forms.CharField(
        label='Email',max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly':'readonly'}
        )
    )
    name = forms.CharField(
        label='Nombres', required=True,
        widget=forms.TextInput( attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(label='Apellidos',required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    institution = forms.CharField(
        label='Institución',required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Teléfono Institucional',required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
