from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from leads.models import Lead

@login_required
def dashboard(request):
    context = {
        'total_customers': Customer.objects.count(),
        'active_customers': Customer.objects.filter(status='active').count(),
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(status='new').count(),
        'hot_leads': Lead.objects.filter(rating='hot').count(),
        'converted_leads': Lead.objects.filter(status='converted').count(),
        'recent_customers': Customer.objects.order_by('-created_at')[:5],
        'recent_leads': Lead.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)