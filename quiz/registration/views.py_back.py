from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from .forms import SignupForm, VerifyForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from .models import VerificationStatus
from django.contrib.auth.models import User
import math, random
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
import string
# Create your views here.




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
    success_url = 'login'

    """
    Checks the form data submitted is valid
    """
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        user_obj = User.objects.get(username=username,email=email)
        user_otp = generate_otp(6)

        
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


        return super().form_valid(form)



class LoginView(FormView):
    """
    A class for login authentication
    """    

    template_name = "registration/login.html"
    form_class = AuthenticationForm
    success_url = 'dashboard'


    def form_valid(self, form):

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        try:
            verify_obj = VerificationStatus.objects.get(user=user)
        except:
            verify_obj = None
        
        if verify_obj and verify_obj.email_verify == False:
            return redirect('registration:otp_verify',user_id=user.id)

        elif user is not None and verify_obj:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
            




def logout_user(request):
    """
    A function defined for user logout
    """
    logout(request)
    return redirect('registration:login')





class VerifyView(FormView):
    """
    A otp verification class
    """
    form_class = VerifyForm
    template_name = "registration/otp_verify.html"
    success_url = "/login"

    def form_valid(self, form):
        user_id = self.kwargs['user_id']
        otp = self.request.POST.get('otp',None)
        user_obj = User.objects.get(id=user_id)
        
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
            return redirect('registration:otp_verify',user_id=user_id)
                

def generate_otp(size):
    """
    A Random OTP generate function with a combination of uppercase,lowecase and digits. 
    It takes one argument size so as to return a value with a size of n number of characters
    """
    generate_otp = ''.join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for n in range (size)])
    return generate_otp
# class Registration(View):
#     form = SignupForm()
    
#     context = {'form':form}
    
#     def get(self, request):
#         return render(request, 'registration/signup.html', self.context)
    
#     def post(self, request):
#         form = SignupForm(request.POST)
        
#         if form.is_valid():

#             form.save()
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             messages.success(request, 'Account created successfully')
            
#             userobj = User.objects.get(username=username,email=email)

#             user_otp = random.randint(100000,999999)

#             VerificationStatus.objects.create(user=userobj,email_otp=user_otp)
            
#             email_content = render_to_string('emails/verification_email.html', locals())

#             email = EmailMultiAlternatives(
#                 "Quiz App Verification", 
#                 email_content, 
#                 settings.EMAIL_HOST_USER,
#                 [str(userobj.email)],
#             )

#             email.attach_alternative(email_content, "text/html")
#             email.send()

#             return redirect('registration:login')
#         return render(request, 'registration/signup.html', self.context)
    


# class Login(View):

#     form = SignupForm()

#     context = {'form':form}


#     def get(self, request):
#         return render(request, 'registration/login.html', self.context)

#     def post(self,request):
#         username = request.POST.get('username')
#         password = request.POST.get('password1')

#         user = authenticate(request, username=username, password=password)

#         try:
#             verify_obj = VerificationStatus.objects.get(user=user)
#         except:
#             verify_obj = None

#         if verify_obj and verify_obj.email_verify == False:
#             return redirect('registration:otp_verify',user_id=user.id)

#         elif user is not None and verify_obj:
#             login(request, user)
#             return redirect('dashboard:user_dashboard')
#         else:
#             messages.info(request, 'Username or password is incorrect')
#             return redirect('dashboard:user_dashboard')
            
#         return render(request,'registration/login.html',locals())
    v