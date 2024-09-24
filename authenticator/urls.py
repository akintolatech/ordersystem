from django.urls import path
from . import views

handler404 = views.page_not_found

app_name = 'authenticator'

urlpatterns = [
    path('edit_estate/<int:estate_id>/', views.edit_estate, name='edit_estate'),
    path('delete_estate_listing/<int:estate_id>/', views.delete_estate_listing, name='delete_estate_listing'),
    path('delete/<int:client_id>', views.delete_client, name="delete_client"),
    path('client_apps/<int:client_id>', views.view_client_application, name="client_apps"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.client_login, name="login"),
    path('logout/', views.purge, name="logout"),
    path('inspect/', views.register, name="register"),
    path('success/', views.success, name="success"),
    path('delete_estate/<int:estate_id>/', views.delete_estate, name='delete_estate'),
    path('realtor/', views.realtor, name="realtor"),
    path('upload/', views.upload_estate, name="upload"),
    path('listings/', views.estate_listings, name="listings"),

]