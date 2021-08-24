from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from registration.models import VerificationStatus

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1' , 'password2']

class VerifyForm(forms.Form):
    # user = forms.CharField()
    class Meta:
        model = VerificationStatus
        fields = ['user','email_verify','email_otp']

