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

    # ── API Explorer ──────────────────────────────────────
    path('api-explorer/', views.api_explorer, name='api_explorer'),

    # Customer CRUD pages
    path('PostAPICustomer/', views.PostAPICustomer, name='PostAPICustomer'),
    path('PutAPICustomer/', views.PutAPICustomer, name='PutAPICustomer'),
    path('DeleteAPICustomer/', views.DeleteAPICustomer, name='DeleteAPICustomer'),

    # Lead CRUD pages
    path('PostAPILead/', views.PostAPILead, name='PostAPILead'),
    path('PutAPILead/', views.PutAPILead, name='PutAPILead'),
    path('DeleteAPILead/', views.DeleteAPILead, name='DeleteAPILead'),

    # Opportunity CRUD pages
    path('PostAPIOpportunity/', views.PostAPIOpportunity, name='PostAPIOpportunity'),
    path('PutAPIOpportunity/', views.PutAPIOpportunity, name='PutAPIOpportunity'),
    path('DeleteAPIOpportunity/', views.DeleteAPIOpportunity, name='DeleteAPIOpportunity'),

    # Interaction CRUD pages
    path('PostAPIInteraction/', views.PostAPIInteraction, name='PostAPIInteraction'),
    path('PutAPIInteraction/', views.PutAPIInteraction, name='PutAPIInteraction'),
    path('DeleteAPIInteraction/', views.DeleteAPIInteraction, name='DeleteAPIInteraction'),

    # Task CRUD pages
    path('PostAPITask/', views.PostAPITask, name='PostAPITask'),
    path('PutAPITask/', views.PutAPITask, name='PutAPITask'),
    path('DeleteAPITask/', views.DeleteAPITask, name='DeleteAPITask'),

    # Ticket CRUD pages
    path('PostAPITicket/', views.PostAPITicket, name='PostAPITicket'),
    path('PutAPITicket/', views.PutAPITicket, name='PutAPITicket'),
    path('DeleteAPITicket/', views.DeleteAPITicket, name='DeleteAPITicket'),
]