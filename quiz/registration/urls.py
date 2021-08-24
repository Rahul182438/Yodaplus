from django.urls import path

from . import views
from .views import RegistrationView, LoginView, VerifyView

app_name = 'registration'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', RegistrationView.as_view(), name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',views.logout_user,name='logout'),
    path('otp_verify/<int:user_id>/',VerifyView.as_view(),name='otp_verify'),
]