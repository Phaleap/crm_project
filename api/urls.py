from django.urls import path
from . import views

urlpatterns = [
    # Summary
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

    # Interactions
    path('interactions/', views.InteractionListCreateAPI.as_view(), name='api_interactions'),
    path('interactions/<int:pk>/', views.InteractionDetailAPI.as_view(), name='api_interaction_detail'),

    # Tasks
    path('tasks/', views.TaskListCreateAPI.as_view(), name='api_tasks'),
    path('tasks/<int:pk>/', views.TaskDetailAPI.as_view(), name='api_task_detail'),

    # Support Tickets
    path('tickets/', views.SupportTicketListCreateAPI.as_view(), name='api_tickets'),
    path('tickets/<int:pk>/', views.SupportTicketDetailAPI.as_view(), name='api_ticket_detail'),
    path('tickets/<int:ticket_pk>/comments/', views.TicketCommentListCreateAPI.as_view(), name='api_ticket_comments'),

    # Users
    path('users/', views.UserListAPI.as_view(), name='api_users'),
]