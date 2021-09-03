from django.urls import path


from .views import DashboardView, QuiestionView, ReportView, save_user_progress

app_name = 'dashboard'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='user_dashboard'),
    path('questions/<str:subject_name>', QuiestionView.as_view(), name='quiz_questions'),    
    path('questions/<str:subject_name>/save/', save_user_progress, name='quiz_progress'),
    path('reports', ReportView.as_view(), name='report'),    
]