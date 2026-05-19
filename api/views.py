from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity
from interactions.models import Interaction
from tasks.models import Task
from support.models import SupportTicket, TicketComment
from accounts.models import User

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
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email', 'company']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CustomerDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


# ── Leads ─────────────────────────────────────────────────
class LeadListCreateAPI(generics.ListCreateAPIView):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email', 'company']

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


class LeadDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


# ── Opportunities ─────────────────────────────────────────
class OpportunityListCreateAPI(generics.ListCreateAPIView):
    queryset = Opportunity.objects.all().order_by('-created_at')
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


class OpportunityDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]


# ── Interactions ──────────────────────────────────────────
class InteractionListCreateAPI(generics.ListCreateAPIView):
    queryset = Interaction.objects.all().order_by('-interaction_date')
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InteractionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]


# ── Tasks ─────────────────────────────────────────────────
class TaskListCreateAPI(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# ── Support Tickets ───────────────────────────────────────
class SupportTicketListCreateAPI(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject', 'ticket_number', 'customer__full_name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SupportTicketDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]


# ── Ticket Comments ───────────────────────────────────────
class TicketCommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketComment.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ticket_id=self.kwargs['ticket_pk'])


# ── Users ─────────────────────────────────────────────────
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]