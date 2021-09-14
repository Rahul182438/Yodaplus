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
from rest_framework.authtoken.models import Token

from django.conf import settings
from registration.models import VerificationStatus
from registration.api.serializers import UserSignupSerializer,VerificationSerializer
from registration.views import generate_otp


class UserCreateApi(APIView):


    def post(self,request):

        """
        User details are fetched and checked for validation
        """
        serializer =  UserSignupSerializer(data=request.data)

        """
        Sucessful response or error responses are stored in data and sent returned when the API is called
        """
        data = {}
        
        if serializer.is_valid():
            
            """
            if user details received are valid an entry is created in User Table and verification email sent
            """
            
            user_details_obj = serializer.save()            
            
            user_otp = generate_otp()

            VerificationStatus.objects.create(user=user_details_obj,email_otp=user_otp)

            email_content = render_to_string('emails/verification_email.html', locals())

            email = EmailMultiAlternatives(
                "Quiz App Verification", 
                email_content, 
                settings.EMAIL_HOST_USER,
                ['rahulkallil3@gmail.com'],
            )
            email.attach_alternative(email_content, "text/html")
            # email.send()
            data['success'] = True
            data['response'] = 'User created and otp send to the registered email.'
            data['username'] = user_details_obj.username
            
            data['token'] = Token.objects.get(user=user_details_obj).key
        else:
            
            data['success'] = False
            data['errors'] = serializer.errors
        
        return Response(data)





class VerificationApi(UpdateAPIView):

    queryset = VerificationStatus.objects.all()
    

    '''
    API for OTP validation.
    '''
    serializer_class = VerificationSerializer
    lookup_field = 'user'

    def get(self, *args, **kwargs):
        """
        Get method used on login to check whether the user loging in has already verified the OTP
        If not he is sent back to the verification page
        """
        username = self.kwargs['user']

        data = {}
        user_obj =User.objects.get(username=username)
        
        try:
            verify_obj = VerificationStatus.objects.get(user=user_obj)
        except:
            verify_obj = None
        
        if verify_obj:
            data['is_verified'] = verify_obj.email_verify
        
        return Response(data)
                

    def post(self,*args,**kwargs):
        
        """
        Entered OTP by user is retrieved and if it matches the one created then the user verification is completed
        """
        username = self.kwargs['user']
        postdata = self.request.data
        
        user_obj =User.objects.get(username=username)
        data = self.request.data
        print(postdata)
        if user_obj:
            try:
                verify_obj = VerificationStatus.objects.get(user=user_obj,email_otp = postdata['otp'])
            except:
                verify_obj = None
            
            data = {}
            if verify_obj:
                verify_obj.email_verify = True
                verify_obj.save()
                data['success'] = True
                data['response'] = "Email Verified"
                return Response(data)
            else:
                data['success'] = False
                data['response'] = "Please enter valid OTP"
        else:
            data['success'] = False
            data['response'] = "User account not found"
            
        return Response(data)
