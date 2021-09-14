from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework.authtoken.views import obtain_auth_token

from registration.api.views import UserCreateApi, VerificationApi


app_name = 'registration'


urlpatterns = [
    path('signup-api/',UserCreateApi.as_view(),name='signup-api'),
    path('login/',obtain_auth_token,name='login'),
    path('verification-api/<str:user>/',VerificationApi.as_view(),name='verification-api'),
] 