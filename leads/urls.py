from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('add/', views.lead_add, name='lead_add'),
    path('<int:pk>/', views.lead_detail, name='lead_detail'),
    path('<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('<int:pk>/delete/', views.lead_delete, name='lead_delete'),
]