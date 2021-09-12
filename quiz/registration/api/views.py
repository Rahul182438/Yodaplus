from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, response
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView


from django.conf import settings
from registration.models import VerificationStatus
from registration.api.serializers import UserSignupSerializer,VerificationSerializer
from registration.views import generate_otp


class UserCreateApi(APIView):

    
    def post(self,request):
       
        serializer =  UserSignupSerializer(data=request.data)
        data = {}
        
        if serializer.is_valid():
            
            
            user_details_obj = serializer.save()            
            
            user_otp = generate_otp()

            VerificationStatus.objects.create(user=user_details_obj,email_otp=user_otp)

            # email_content = render_to_string('emails/verification_email.html', locals())

            # email = EmailMultiAlternatives(
            #     "Quiz App Verification", 
            #     email_content, 
            #     settings.EMAIL_HOST_USER,
            #     ['rahulkallil3@gmail.com'],
            # )
            # email.attach_alternative(email_content, "text/html")
            # email.send()
            data['success'] = True
            data['response'] = 'User created and otp send to the registered email.'
            data['username'] = user_details_obj.username
            
        else:
            
            data['success'] = False
            data['errors'] = serializer.errors
        
        return Response(data)





class VerificationApi(UpdateAPIView):

    queryset = VerificationStatus.objects.all()
    

    # queryset = VerificationStatus.objects.filter(user=user_obj)
    serializer_class = VerificationSerializer
    lookup_field = 'user'

    def put(self,*args,**kwargs):
        
        username = self.kwargs['user']
        user_obj =User.objects.get(username=username)
        data = self.request.data
        if user_obj:
            try:
                obj = VerificationStatus.objects.get(user=user_obj,email_otp =int(data['email_otp']))
            except:
                obj = None
            
            data = {}
            if obj:
                obj.email_verify = True
                obj.save()
                data['response'] = "Email Verified"
                return Response(data)
            else:
                data['response'] = "Please enter valid OTP"
        else:
            data['response'] = "User account not found"
            
        return Response(data)
