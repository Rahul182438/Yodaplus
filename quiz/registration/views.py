from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import SignupForm, VerifyForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import VerificationStatus
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.


def index(request, template_name="index.html"):
    return render(request, template_name)


class Registration(View):
    form = SignupForm()
    
    context = {'form':form}
    
    def get(self, request):
        return render(request, 'registration/signup.html', self.context)
    
    def post(self, request):
        form = SignupForm(request.POST)
        
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account created successfully')
            
            userobj = User.objects.get(username=username,email=email)

            user_otp = random.randint(100000,999999)

            VerificationStatus.objects.create(user=userobj,email_otp=user_otp)
            
            email_content = render_to_string('emails/verification_email.html', locals())

            email = EmailMultiAlternatives(
                "Quiz App Verification", 
                email_content, 
                settings.EMAIL_HOST_USER,
                [str(userobj.email)],
            )

            email.attach_alternative(email_content, "text/html")
            email.send()

            return redirect('registration:login')
        return render(request, 'registration/signup.html', self.context)
    
class Login(View):

    form = SignupForm()

    context = {'form':form}


    def get(self, request):
        return render(request, 'registration/login.html', self.context)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        try:
            verify_obj = VerificationStatus.objects.get(user=user)
        except:
            verify_obj = None

        if verify_obj and verify_obj.email_verify == False:
            return redirect('registration:otp_verify',user_id=user.id)

        elif user is not None and verify_obj:
            login(request, user)
            return redirect('dashboard:user_dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('dashboard:user_dashboard')
            
        return render(request,'registration/login.html',locals())
    


def logout_user(request):
    logout(request)
    return redirect('registration:login')

class Verify(View):
    form = VerifyForm()

    context = {'form':form}

    def get(self, request,user_id):
        return render(request, 'registration/otp_verify.html', self.context)

    def post(self,request,user_id):
       
        otp = request.POST.get('otp',None)
        print(otp)
        userobj = User.objects.get(id=user_id)
        
        if userobj:
            try:
                verify_obj = VerificationStatus.objects.get(user=userobj)
            except:
                verify_obj = None

        if otp and verify_obj and verify_obj.email_otp == int(otp):
            verify_obj.email_verify = True
            verify_obj.save()
            # user = authenticate(request, username=userobj.username, password=userobj.password)

            
            # return redirect('dashboard:user_dashboard')
            return redirect('registration:login')
        else:
            messages.info(request, 'OTP is incorrect')
            return redirect('registration:otp_verify',user_id=user_id)
            
        return render(request,'registration/otp_verify.html',locals())
    

