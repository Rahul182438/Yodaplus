from django.urls import path

from . import views
from .views import Registration, Login, Verify

app_name = 'registration'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', Registration.as_view(), name='register'),
    path('login',Login.as_view(),name='login'),
    path('otp_verify/<int:user_id>/',Verify.as_view(),name='otp_verify')
]