from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('terms/', views.legal, name='legal'),
    #Admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_order_item/<int:order_item_id>', views.delete_order_item, name='delete_order_item'),
    path('view_customer_order/<int:order_item_id>', views.view_customer_order, name='view_customer_order'),


]