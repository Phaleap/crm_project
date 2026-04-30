from django.db import models
from accounts.models import User

class CustomerTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    SEGMENT_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('smb', 'SMB'),
        ('startup', 'Startup'),
        ('individual', 'Individual'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    segment = models.CharField(max_length=20, choices=SEGMENT_CHOICES, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    tags = models.ManyToManyField(CustomerTag, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_customers')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name