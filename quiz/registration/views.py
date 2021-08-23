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
            text_content = strip_tags(email_content)

            email = EmailMultiAlternatives(
                "Quiz App Verification", 
                email_content, 
                settings.EMAIL_HOST_USER,
                ['rahulkallil3@gmail.com'],
            )

            email.attach_alternative(email_content, "text/html")
            email.send()
            # send_mail("Quiz App Verification", 
            #     email_content, 
                
            #     ['rahulkallil3@gmail.com'], 
            #     fail_silently = False
            #     )

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
        print(username)
        print(password)
        otp = request.POST.get('otp')
        # if otp:
            
        user = authenticate(request, username=username, password=password)
        print(user)
        try:
            verify_obj = VerificationStatus.objects.get(user=user)
        except:
            verify_obj = None
        print(verify_obj)
        if verify_obj and verify_obj.email_verify == False:
            return redirect('registration:otp_verify',user_id=user.id)
            # verify_obj.email_verify = True
            # verify_obj.save()
            # if user is not None:
            # login(request, user)         
            
        elif user is not None and verify_obj:
            login(request, user)
            return redirect('dashboard:user_dashboard')
        else:
            messages.info(request, 'Username,password or OTP is incorrect')
            
        return render(request,'registration/login.html',locals())
    

class Verify(View):
    form = VerifyForm()

    context = {'form':form}

    def get(self, request,user_id):
        return render(request, 'registration/otp_verify.html', self.context)

    def post(self,request,user_id):
        otp = int(request.POST.get('otp'))
        
        userobj = User.objects.get(id=user_id)
        print(userobj)
        if userobj:
            try:
                verify_obj = VerificationStatus.objects.get(user=userobj)
            except:
                verify_obj = None

        if otp and verify_obj and verify_obj.email_otp == otp:
            verify_obj.email_verify = True
            verify_obj.save()
            user = authenticate(request, username=userobj.username, password=userobj.password)
            login(request, user)
            
            return redirect('dashboard:user_dashboard')
        else:
            messages.info(request, 'OTP is incorrect')
            
        return render(request,'registration/otp_verify.html',locals())
    

