from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from customers.models import Customer
from leads.models import Lead
from accounts.models import User
from .serializers import CustomerSerializer, LeadSerializer, UserSerializer

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

# ── User API ──────────────────────────────────────────────
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]