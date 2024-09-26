from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [

    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('', views.user_login, name='login'),
    # path('logout', views.user_logout, name='logout'),
    path('', include('django.contrib.auth.urls')),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
]