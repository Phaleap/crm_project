from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from .forms import OpportunityForm
from .models import Opportunity

@login_required
def opportunity_list(request):
    query = request.GET.get('q', '')
    stage = request.GET.get('stage', '')

    opportunities = Opportunity.objects.all().order_by('-created_at')

    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query) |
            Q(customer__full_name__icontains=query)
        )
    if stage:
        opportunities = opportunities.filter(stage=stage)

    total_value = opportunities.aggregate(Sum('value'))['value__sum'] or 0

    context = {
        'opportunities': opportunities,
        'query': query,
        'stage': stage,
        'total': opportunities.count(),
        'total_value': total_value,
        'won': opportunities.filter(stage='closed_won').count(),
        'lost': opportunities.filter(stage='closed_lost').count(),
    }
    return render(request, 'opportunities/opportunity_list.html', context)

@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, 'opportunities/opportunity_detail.html', {'opportunity': opportunity})

@login_required
def opportunity_add(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.assigned_to = request.user
            opportunity.save()
            return redirect('opportunity_list')
    else:
        form = OpportunityForm()
    return render(request, 'opportunities/opportunity_add.html', {'form': form})

@login_required
def opportunity_edit(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect('opportunity_detail', pk=pk)
    else:
        form = OpportunityForm(instance=opportunity)
    return render(request, 'opportunities/opportunity_edit.html', {
        'opportunity': opportunity,
        'form': form,
    })

@login_required
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        opportunity.delete()
        return redirect('opportunity_list')
    return render(request, 'opportunities/opportunity_confirm_delete.html', {'opportunity': opportunity})
