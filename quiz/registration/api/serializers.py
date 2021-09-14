from os import write
from registration.models import VerificationStatus
from rest_framework import serializers
from django.contrib.auth.models import User



class UserSignupSerializer(serializers.ModelSerializer):
    """
    confirm password field and email is a required field for user signup
    """
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    email = serializers.EmailField(required=True)    
    class Meta:
        model = User
        fields = ['username', 'email', 'password' , 'password2']

        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate_email(self, email):
        """
        If entered email is already present in the database validaton error is thrown
        """

        email_obj = User.objects.filter(email=email).first()
        if email_obj:
            raise serializers.ValidationError("Email is already used")
        return email

    def validate(self,data):
        """
        To check whether the password entered in both the fields are matched
        """
        if not data.get('password') or not data.get('password2'):
            
            raise serializers.ValidationError("Please enter a password.")
        if data.get('password') != data.get('password2'):
            
            raise serializers.ValidationError("Those passwords don't match.")
        return data        


    def save(self):

        """
        If all fields are validated a user entry is created.
        """
        user_obj = User(
                    username=self.validated_data['username'],
                    email=self.validated_data['email'],
                )

        password = self.validated_data['password']
        user_obj.set_password(password)
        user_obj.save()
    
        return user_obj




class VerificationSerializer(serializers.ModelSerializer):
    """
    OTP verification serializer. A OTP input field is required
    """
    email_otp = serializers.CharField(max_length=6,required=True)
    class Meta:
        model = VerificationStatus
        fields = ['email_otp']

