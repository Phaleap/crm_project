from django.urls import path
from . import views

urlpatterns = [
    path('roles/', views.role_list, name='role_list'),
    path('roles/add/', views.role_add, name='role_add'),
    path('roles/<int:pk>/edit/', views.role_edit, name='role_edit'),
    path('roles/<int:pk>/delete/', views.role_delete, name='role_delete'),
    
]