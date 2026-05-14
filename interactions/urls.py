from django.urls import path
from . import views

urlpatterns = [
    path('', views.interaction_list, name='interaction_list'),
    path('add/<int:customer_pk>/', views.interaction_add, name='interaction_add'),
    path('<int:pk>/delete/', views.interaction_delete, name='interaction_delete'),
]