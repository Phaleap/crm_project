from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('add/', views.opportunity_add, name='opportunity_add'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('<int:pk>/edit/', views.opportunity_edit, name='opportunity_edit'),
    path('<int:pk>/delete/', views.opportunity_delete, name='opportunity_delete'),
]