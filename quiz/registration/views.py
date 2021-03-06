from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http.response import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

import pyotp

from .models import VerificationStatus
from .forms import SignupForm, VerifyForm
from .decorators import user_is_logged_in

class IndexView(TemplateView):

    """
    Purpose - A welcome page created.
    A function is called with 2 parameters request and template_name
    template_name has the value of html file name that needs to be rendered.

    """
    template_name = "index.html"
    


class RegistrationView(FormView):

    """
    A FormView class is written for the signup process

    """    
    template_name = "registration/signup.html"
    form_class = SignupForm
    # success_url = 'otp_verify'

    """
    Checks the form data submitted is valid
    """
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        user_obj = User.objects.get(username=username,email=email)
        user_otp = generate_otp()

        
        VerificationStatus.objects.create(user=user_obj,email_otp=user_otp)
        
        email_content = render_to_string('emails/verification_email.html', locals())

        email = EmailMultiAlternatives(
            "Quiz App Verification", 
            email_content, 
            settings.EMAIL_HOST_USER,
            ['rahulkallil3@gmail.com'],
        )

        email.attach_alternative(email_content, "text/html")
        email.send()
        return redirect('registration:otp_verify',username=user_obj.username)





@method_decorator(user_is_logged_in,name='dispatch')
class LoginFormView(LoginView):
    
    template_name = "registration/login.html"

    def form_valid(self, form):

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        try:
            verify_obj = VerificationStatus.objects.get(user=user)
        except:
            verify_obj = None
        
        if verify_obj and verify_obj.email_verify == False:
            return redirect('registration:otp_verify',username=user.username)

        elif user is not None and verify_obj:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("#####")
        messages.info(self.request, 'Please enter a correct username and password')
        return super().form_invalid(form)


@method_decorator(user_is_logged_in,name='dispatch')
class VerifyView(FormView):
    """
    A otp verification class
    """
    form_class = VerifyForm
    template_name = "registration/otp_verify.html"
    success_url = reverse_lazy("registration:login")

    def form_valid(self, form):
        name = self.kwargs['username']
        otp = self.request.POST.get('otp',None)
        user_obj = User.objects.get(username=name)
        
        if user_obj:
            try:
                verify_obj = VerificationStatus.objects.get(user=user_obj)
            except:
                verify_obj = None

        if otp and verify_obj and verify_obj.email_otp == otp:
            verify_obj.email_verify = True
            verify_obj.save()
            return HttpResponseRedirect(self.get_success_url())
        
        else:
            messages.info(self.request, 'OTP is incorrect')
            return redirect('registration:otp_verify',user_id=user_obj.username)
                

def generate_otp():
    """
    A  OTP generate function.
    OTP generated with PyOTP library with the current timestamp
    """
    totp = pyotp.TOTP('base32secret3232')
    generate_otp  = totp.now()

    return generate_otp
