from django.urls import path
from django.urls.resolvers import URLPattern

from dashboard.api.views import DashboardApiView, QuestionApiView, UserProgressApiView, AnswersApiView, ReportApiView, UserProgressTimeApiView

app_name = 'dashboard'

urlpatterns = [
    path('dashboard',DashboardApiView.as_view(),name='dashboard'),
    path('questions/<str:url_slug>', QuestionApiView.as_view(), name='quiz_questions'),
    path('user_progress/', UserProgressApiView.as_view(), name='quiz_progress'),
    path('answers/<str:question_id>', AnswersApiView.as_view(), name='quiz_answers'),
    path('reports/<str:url_slug>', ReportApiView.as_view(), name='quiz_reports'),
    path('time/', UserProgressTimeApiView.as_view(), name='progress_time'),
]