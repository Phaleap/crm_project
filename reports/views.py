from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from accounts.permissions import admin_required
from accounts.models import User
from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity
from interactions.models import Interaction
from tasks.models import Task
from support.models import SupportTicket

@login_required
def dashboard(request):
    role = getattr(request.user, 'role', 'sales_staff')
    role_label = 'Admin' if request.user.is_superuser else request.user.get_role_display()

    context = {
        'role': role,
        'role_label': role_label,
        'total_customers': Customer.objects.count(),
        'active_customers': Customer.objects.filter(status='active').count(),
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(status='new').count(),
        'hot_leads': Lead.objects.filter(rating='hot').count(),
        'converted_leads': Lead.objects.filter(status='converted').count(),
        'total_opportunities': Opportunity.objects.count(),
        'open_opportunities': Opportunity.objects.exclude(stage__in=['closed_won', 'closed_lost']).count(),
        'closed_won': Opportunity.objects.filter(stage='closed_won').count(),
        'pipeline_value': Opportunity.objects.exclude(stage__in=['closed_won', 'closed_lost']).aggregate(total=Sum('value'))['total'] or 0,
        'total_interactions': Interaction.objects.count(),
        'total_tasks': Task.objects.count(),
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'overdue_tasks': Task.objects.filter(status__in=['pending', 'in_progress'], due_date__lt=timezone.localdate()).count(),
        'total_tickets': SupportTicket.objects.count(),
        'open_tickets': SupportTicket.objects.filter(status='open').count(),
        'urgent_tickets': SupportTicket.objects.filter(priority='urgent').count(),
        'resolved_tickets': SupportTicket.objects.filter(status='resolved').count(),
        'total_users': User.objects.count(),
        'recent_customers': Customer.objects.order_by('-created_at')[:5],
        'recent_leads': Lead.objects.order_by('-created_at')[:5],
        'recent_opportunities': Opportunity.objects.order_by('-created_at')[:5],
        'recent_tasks': Task.objects.select_related('assigned_to').order_by('-created_at')[:5],
        'recent_tickets': SupportTicket.objects.select_related('customer').order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)

@login_required
@admin_required
def api_explorer(request):
    return render(request, 'api_explorer/api_explorer.html')
