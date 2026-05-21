from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.api_summary, name='api_summary'),

    # Customers
    path('customers/', views.CustomerListCreateAPI.as_view(), name='api_customers'),
    path('customers/<int:pk>/', views.CustomerDetailAPI.as_view(), name='api_customer_detail'),

    # Leads
    path('leads/', views.LeadListCreateAPI.as_view(), name='api_leads'),
    path('leads/<int:pk>/', views.LeadDetailAPI.as_view(), name='api_lead_detail'),

    # Opportunities
    path('opportunities/', views.OpportunityListCreateAPI.as_view(), name='api_opportunities'),
    path('opportunities/<int:pk>/', views.OpportunityDetailAPI.as_view(), name='api_opportunity_detail'),

    # Users
    path('users/', views.UserListAPI.as_view(), name='api_users'),
    # Interactions
    path('interactions/', views.InteractionViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_interactions'),
    path('interactions/<int:pk>/', views.InteractionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api_interaction_detail'),
    # Tasks
    path('tasks/', views.TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_tasks'),
    path('tasks/<int:pk>/', views.TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api_task_detail'),
    # Support Tickets
    path('support-tickets/', views.SupportTicketViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_support_tickets'),
    path('support-tickets/<int:pk>/', views.SupportTicketViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api_support_ticket_detail'),

    # Category REST API
    path('APICategoryLC/', views.APICategoryLC.as_view(), name='APICategoryLC'),
    path('APICategoryLC/<int:pk>/', views.APICategoryRUD.as_view(), name='APICategoryRUD'),

    # Category page views
    path('PostAPICategory/', views.PostAPICategory, name='PostAPICategory'),
    path('PutAPICategory/', views.PutAPICategory, name='PutAPICategory'),
    path('DeleteAPICategory/', views.DeleteAPICategory, name='DeleteAPICategory'),
]