from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from .views import IndexView, RegistrationView, LoginFormView, VerifyView


app_name = 'registration'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup', RegistrationView.as_view(), name='register'),
    path('login',LoginFormView.as_view(),name='login'),
    path('logout',LogoutView.as_view(next_page=reverse_lazy('registration:login')),name='logout'),
    path('otp_verify/<str:username>/',VerifyView.as_view(),name='otp_verify'),
]