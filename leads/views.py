from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.permissions import sales_required
from .models import Lead

@login_required
@sales_required
def lead_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    rating = request.GET.get('rating', '')

    leads = Lead.objects.all().order_by('-created_at')

    if query:
        leads = leads.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )
    if status:
        leads = leads.filter(status=status)
    if rating:
        leads = leads.filter(rating=rating)

    context = {
        'leads': leads,
        'query': query,
        'status': status,
        'rating': rating,
        'total': leads.count(),
    }
    return render(request, 'leads/lead_list.html', context)

@login_required
@sales_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'leads/lead_detail.html', {'lead': lead})

@login_required
@sales_required
def lead_add(request):
    if request.method == 'POST':
        Lead.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            company=request.POST.get('company'),
            source=request.POST.get('source'),
            status=request.POST.get('status', 'new'),
            rating=request.POST.get('rating'),
            budget=request.POST.get('budget') or None,
            notes=request.POST.get('notes'),
            assigned_to=request.user,
        )
        return redirect('lead_list')
    return render(request, 'leads/lead_add.html')

@login_required
@sales_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.full_name = request.POST.get('full_name')
        lead.email = request.POST.get('email')
        lead.phone = request.POST.get('phone')
        lead.company = request.POST.get('company')
        lead.source = request.POST.get('source')
        lead.status = request.POST.get('status', 'new')
        lead.rating = request.POST.get('rating')
        lead.budget = request.POST.get('budget') or None
        lead.notes = request.POST.get('notes')
        lead.save()
        return redirect('lead_detail', pk=pk)
    return render(request, 'leads/lead_edit.html', {'lead': lead})

@login_required
@sales_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        return redirect('lead_list')
    return render(request, 'leads/lead_confirm_delete.html', {'lead': lead})
