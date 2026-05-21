

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity
from accounts.models import User
from interactions.models import Interaction
from tasks.models import Task
from support.models import SupportTicket
from .models import Category
from .serializers import (
    CustomerSerializer, LeadSerializer, OpportunitySerializer,
    SupportTicketSerializer, TaskSerializer, UserSerializer,
    InteractionSerializer, CategorySerializer,
)

# ── Summary endpoint ──────────────────────────────────────
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
    })

# ── Customer API ──────────────────────────────────────────
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

# ── Lead API ──────────────────────────────────────────────
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

# ── Opportunity API ───────────────────────────────────────
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

# ── User API ──────────────────────────────────────────────
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
# ── Category REST API ─────────────────────────────────────
class APICategoryLC(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer

class APICategoryRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ── Category page views ───────────────────────────────────
def PostAPICategory(request):
    return render(request, 'PostAPICategory.html')

def PutAPICategory(request):
    return render(request, 'PutAPICategory.html')

def DeleteAPICategory(request):
    return render(request, 'DeleteAPICategory.html')
