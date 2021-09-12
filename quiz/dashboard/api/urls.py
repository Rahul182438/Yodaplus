

from django.urls import path
from django.urls.resolvers import URLPattern

from dashboard.api.views import DashboardApiView, QuestionApiView, UserProgressApiView

app_name = 'dashboard'

urlpatterns = [
    path('dashboard',DashboardApiView.as_view(),name='dashboard'),
    path('questions/<str:url_slug>', QuestionApiView.as_view(), name='quiz_questions'),
    path('questions/<str:url_slug>/save', UserProgressApiView.as_view(), name='quiz_progress'),
]