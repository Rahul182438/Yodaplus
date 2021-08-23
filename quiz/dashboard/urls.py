from django.urls import path

from . import views
from .views import Dashboard

app_name = 'dashboard'

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='user_dashboard'),
]