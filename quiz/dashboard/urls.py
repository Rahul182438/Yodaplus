from django.urls import path


from .views import DashboardView, QuiestionView

app_name = 'dashboard'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='user_dashboard'),
    path('questions/<int:pk>/<int:type_id>', QuiestionView.as_view(), name='quiz_questions'),    
]