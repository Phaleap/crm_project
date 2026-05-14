from rest_framework import serializers
from customers.models import Customer, CustomerTag
from leads.models import Lead
from opportunities.models import Opportunity
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone']

class CustomerTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerTag
        fields = ['id', 'name', 'color']

class CustomerSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )
    tags = CustomerTagSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'email', 'phone', 'company',
            'job_title', 'segment', 'industry', 'city', 'country',
            'status', 'tags', 'assigned_to', 'assigned_to_id',
            'created_at', 'updated_at'
        ]

class LeadSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )

    class Meta:
        model = Lead
        fields = [
            'id', 'full_name', 'email', 'phone', 'company',
            'source', 'status', 'rating', 'budget', 'notes',
            'assigned_to', 'assigned_to_id',
            'converted_at', 'created_at', 'updated_at'
        ]

class OpportunitySerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, required=False
    )
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    lead_name = serializers.CharField(source='lead.full_name', read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'customer', 'customer_name', 'lead', 'lead_name',
            'stage', 'value', 'probability',
            'expected_close_date', 'actual_close_date',
            'loss_reason', 'assigned_to', 'assigned_to_id',
            'notes', 'created_at', 'updated_at'
        ]