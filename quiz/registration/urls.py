from django.urls import path, reverse_lazy
from . import views
from .views import IndexView, RegistrationView, LoginFormView, VerifyView
from django.contrib.auth.views import LogoutView

app_name = 'registration'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup', RegistrationView.as_view(), name='register'),
    path('login',LoginFormView.as_view(),name='login'),
    # path('logout',views.logout_user,name='logout'),
    path('logout',LogoutView.as_view(next_page=reverse_lazy('registration:login')),name='logout'),
    path('otp_verify/<int:user_id>/',VerifyView.as_view(),name='otp_verify'),
]