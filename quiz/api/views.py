from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

class SignupApiView(TemplateView):

    """
    Purpose - A welcome page created.
    A function is called with 2 parameters request and template_name
    template_name has the value of html file name that needs to be rendered.

    """
    template_name = "api/registration/signup.html"


class LoginApiView(TemplateView):

    template_name = "api/registration/login.html"

class VerificationApiView(TemplateView):
    
    template_name = "api/registration/otp_verify.html"
