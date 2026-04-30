from django.db import models
from accounts.models import User
from customers.models import Customer

class Lead(models.Model):
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('cold_call', 'Cold Call'),
        ('event', 'Event'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('unqualified', 'Unqualified'),
        ('converted', 'Converted'),
    ]
    RATING_CHOICES = [
        ('hot', '🔥 Hot'),
        ('warm', '😊 Warm'),
        ('cold', '❄️ Cold'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    converted_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    converted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} [{self.get_status_display()}]"