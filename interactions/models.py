from django.db import models
from accounts.models import User
from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity


class Interaction(models.Model):
    TYPE_CHOICES = [
        ('phone_call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('chat', 'Chat'),
        ('site_visit', 'Site Visit'),
    ]
    DIRECTION_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ]
    OUTCOME_CHOICES = [
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('callback', 'Callback'),
        ('demo_requested', 'Demo Requested'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='interactions')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, null=True, blank=True, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='interactions')

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, blank=True)
    interaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-interaction_date']

    def __str__(self):
        return f"{self.get_type_display()} with {self.customer} on {self.interaction_date:%Y-%m-%d}"