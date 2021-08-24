from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, VerifyForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from .models import VerificationStatus
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
# Create your views here.


def index(request, template_name="index.html"):
    return render(request, template_name)



class RegistrationView(FormView):
    
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = 'login'


    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        userobj = User.objects.get(username=username,email=email)

        user_otp = random.randint(100000,999999)

        VerificationStatus.objects.create(user=userobj,email_otp=user_otp)
        
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
    logout(request)
    return redirect('registration:login')


class VerifyView(FormView):
    form_class = VerifyForm
    template_name = "registration/otp_verify.html"
    success_url = "/login"

    def form_valid(self, form):
        user_id = self.kwargs['user_id']
        otp = self.request.POST.get('otp',None)
        userobj = User.objects.get(id=user_id)
        
        if userobj:
            try:
                verify_obj = VerificationStatus.objects.get(user=userobj)
            except:
                verify_obj = None

        if otp and verify_obj and verify_obj.email_otp == int(otp):
            verify_obj.email_verify = True
            verify_obj.save()
            return HttpResponseRedirect(self.get_success_url())
        
        else:
            messages.info(self.request, 'OTP is incorrect')
            return redirect('registration:otp_verify',user_id=user_id)
                

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
    