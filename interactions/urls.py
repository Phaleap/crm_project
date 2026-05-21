from django.urls import path
from . import views

urlpatterns = [
    path('', views.interaction_list, name='interaction_list'),
    path('add/', views.interaction_add, name='interaction_add'),
    path('add/<int:customer_pk>/', views.interaction_add, name='interaction_add_customer'),
    path('<int:pk>/edit/', views.interaction_edit, name='interaction_edit'),
    path('<int:pk>/delete/', views.interaction_delete, name='interaction_delete'),
]