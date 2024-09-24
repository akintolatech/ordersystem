from django.urls import path
from . import views

handler404 = views.page_not_found

app_name = 'browser'

urlpatterns = [
    path('', views.index, name="index"),
    path('detail/<int:estate_id>', views.detail, name="detail"),
    path('detail-app/<int:estate_id>', views.detail_app, name="detail-app"),
    path('legal/', views.legal, name="legal"),
]