from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

# app_name = "account"

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]