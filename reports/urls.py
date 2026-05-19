from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api-explorer/', views.api_explorer, name='api_explorer'),
]