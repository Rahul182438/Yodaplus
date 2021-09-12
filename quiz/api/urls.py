from django.urls import path


from .views import SignupApiView, LoginApiView, VerificationApiView

app_name = 'api'

urlpatterns = [
    
    path('signup-api', SignupApiView.as_view(), name='register'),
    path('login-api',LoginApiView.as_view(),name='login'),
    path('otp-api/user=<str:username>/', VerificationApiView.as_view(), name='verify'),
    

]
