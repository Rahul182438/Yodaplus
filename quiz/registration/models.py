from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class VerificationStatus(models.Model):
    """
    Model for OTP storing and verification
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email_verify = models.BooleanField(default=False)
    email_otp =  models.CharField(max_length=6)

    def __str__(self):
        return str(self.user.username)