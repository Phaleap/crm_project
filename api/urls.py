from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.api_summary, name='api_summary'),
    path('customers/', views.CustomerListCreateAPI.as_view(), name='api_customers'),
    path('customers/<int:pk>/', views.CustomerDetailAPI.as_view(), name='api_customer_detail'),
    path('leads/', views.LeadListCreateAPI.as_view(), name='api_leads'),
    path('leads/<int:pk>/', views.LeadDetailAPI.as_view(), name='api_lead_detail'),
    path('users/', views.UserListAPI.as_view(), name='api_users'),
]