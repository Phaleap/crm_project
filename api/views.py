from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity
from interactions.models import Interaction
from tasks.models import Task
from support.models import SupportTicket, TicketComment
from accounts.models import User
from accounts.permissions import (
    IsAdminRole, IsSalesRole, IsServiceRole, IsSalesOrServiceRole,
    admin_required
)

from .serializers import (
    CustomerSerializer, LeadSerializer, OpportunitySerializer,
    InteractionSerializer, TaskSerializer,
    SupportTicketSerializer, TicketCommentSerializer,
    UserSerializer
)


# ── Summary ───────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_summary(request):
    return Response({
        'total_customers': Customer.objects.count(),
        'active_customers': Customer.objects.filter(status='active').count(),
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(status='new').count(),
        'hot_leads': Lead.objects.filter(rating='hot').count(),
        'converted_leads': Lead.objects.filter(status='converted').count(),
        'total_opportunities': Opportunity.objects.count(),
        'closed_won': Opportunity.objects.filter(stage='closed_won').count(),
        'closed_lost': Opportunity.objects.filter(stage='closed_lost').count(),
        'total_interactions': Interaction.objects.count(),
        'total_tasks': Task.objects.count(),
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'total_tickets': SupportTicket.objects.count(),
        'open_tickets': SupportTicket.objects.filter(status='open').count(),
    })


# ── Customers ─────────────────────────────────────────────
class CustomerListCreateAPI(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsSalesOrServiceRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email', 'company']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CustomerDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsSalesOrServiceRole]


# ── Leads ─────────────────────────────────────────────────
class LeadListCreateAPI(generics.ListCreateAPIView):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [IsSalesRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email', 'company']

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


class LeadDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsSalesRole]


# ── Opportunities ─────────────────────────────────────────
class OpportunityListCreateAPI(generics.ListCreateAPIView):
    queryset = Opportunity.objects.all().order_by('-created_at')
    serializer_class = OpportunitySerializer
    permission_classes = [IsSalesRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


class OpportunityDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsSalesRole]


# ── Interactions ──────────────────────────────────────────
class InteractionListCreateAPI(generics.ListCreateAPIView):
    queryset = Interaction.objects.all().order_by('-interaction_date')
    serializer_class = InteractionSerializer
    permission_classes = [IsSalesOrServiceRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InteractionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsSalesOrServiceRole]


# ── Tasks ─────────────────────────────────────────────────
class TaskListCreateAPI(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsSalesRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsSalesRole]


# ── Support Tickets ───────────────────────────────────────
class SupportTicketListCreateAPI(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer
    permission_classes = [IsServiceRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject', 'ticket_number', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SupportTicketDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsServiceRole]


class TicketCommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsServiceRole]

    def get_queryset(self):
        return TicketComment.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ticket_id=self.kwargs['ticket_pk'])


# ── Users ─────────────────────────────────────────────────
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]


# ══════════════════════════════════════════════════════════
# Template render views for API Explorer CRUD pages
# ══════════════════════════════════════════════════════════

@login_required
@admin_required
def api_explorer(request):
    return render(request, 'api_explorer/api_explorer.html')

# ── Customer pages ────────────────────────────────────────
@login_required
def PostAPICustomer(request):
    return render(request, 'api_explorer/customers/post_customer.html')

@login_required
def PutAPICustomer(request):
    return render(request, 'api_explorer/customers/put_customer.html')

@login_required
def DeleteAPICustomer(request):
    return render(request, 'api_explorer/customers/delete_customer.html')

# ── Lead pages ────────────────────────────────────────────
@login_required
def PostAPILead(request):
    return render(request, 'api_explorer/leads/post_lead.html')

@login_required
def PutAPILead(request):
    return render(request, 'api_explorer/leads/put_lead.html')

@login_required
def DeleteAPILead(request):
    return render(request, 'api_explorer/leads/delete_lead.html')

# ── Opportunity pages ─────────────────────────────────────
@login_required
def PostAPIOpportunity(request):
    return render(request, 'api_explorer/opportunities/post_opportunity.html')

@login_required
def PutAPIOpportunity(request):
    return render(request, 'api_explorer/opportunities/put_opportunity.html')

@login_required
def DeleteAPIOpportunity(request):
    return render(request, 'api_explorer/opportunities/delete_opportunity.html')

# ── Interaction pages ─────────────────────────────────────
@login_required
def PostAPIInteraction(request):
    return render(request, 'api_explorer/interactions/post_interaction.html')

@login_required
def PutAPIInteraction(request):
    return render(request, 'api_explorer/interactions/put_interaction.html')

@login_required
def DeleteAPIInteraction(request):
    return render(request, 'api_explorer/interactions/delete_interaction.html')

# ── Task pages ────────────────────────────────────────────
@login_required
def PostAPITask(request):
    return render(request, 'api_explorer/tasks/post_task.html')

@login_required
def PutAPITask(request):
    return render(request, 'api_explorer/tasks/put_task.html')

@login_required
def DeleteAPITask(request):
    return render(request, 'api_explorer/tasks/delete_task.html')

# ── Ticket pages ──────────────────────────────────────────
@login_required
def PostAPITicket(request):
    return render(request, 'api_explorer/tickets/post_ticket.html')

@login_required
def PutAPITicket(request):
    return render(request, 'api_explorer/tickets/put_ticket.html')

@login_required
def DeleteAPITicket(request):
    return render(request, 'api_explorer/tickets/delete_ticket.html')
