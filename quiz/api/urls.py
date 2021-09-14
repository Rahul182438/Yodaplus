
from django.urls import path


from .views import SignupApiView, LoginApiView, VerificationApiView, DashboardView, QuestionsView

app_name = 'api'

urlpatterns = [
    
    path('signup-api', SignupApiView.as_view(), name='register'),
    path('login-api',LoginApiView.as_view(),name='login'),
    path('otp-api/user=<str:username>/', VerificationApiView.as_view(), name='verify'),
    path('dashboard-api/', DashboardView.as_view(), name='dashboard-api'),
    path('questions-api/<str:subject_name>', QuestionsView.as_view(), name='question-api'),
    

]
