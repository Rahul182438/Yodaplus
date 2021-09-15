from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from registration.models import VerificationStatus

class SignupForm(UserCreationForm):
    """
    User Signup form created.
    Email field is kept as mandatory to send the OTP for verification
    """
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1' , 'password2']

class VerifyForm(forms.Form):
    """
    A Verification form created to use the email otp field.
    """
    class Meta:
        model = VerificationStatus
        fields = ['user','email_verify','email_otp']

