from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class VerificationStatus(models.Model):
    """
    Model for OTP storing and verification
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email_verify = models.BooleanField(default=False)
    email_otp =  models.CharField(max_length=16)

    def __str__(self):
        return str(self.user.username)



@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
