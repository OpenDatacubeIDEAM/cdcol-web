from django import forms

class SignupForm(forms.Form):
    is_analyst = forms.BooleanField(label='Analista')
    is_developer = forms.BooleanField(label='Desarrollador')

    def signup(self, request, user):
        user.is_analyst = True
        user.is_developer = True
        user.save()