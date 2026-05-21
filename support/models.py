from django.db import models
from django.conf import settings
from customers.models import Customer
import uuid


def generate_ticket_number():
    return 'TKT-' + str(uuid.uuid4()).upper()[:8]


class SupportTicket(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('inquiry', 'Inquiry'),
        ('technical', 'Technical Issue'),
        ('billing', 'Billing'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    ticket_number = models.CharField(max_length=20, unique=True, default=generate_ticket_number, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES, default='inquiry')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.ticket_number} - {self.subject}'


class TicketComment(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment on {self.ticket.ticket_number} by {self.author}'