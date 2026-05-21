from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Interaction
from customers.models import Customer


@login_required
def interaction_list(request):
    query = request.GET.get('q', '')
    type_filter = request.GET.get('type', '')

    interactions = Interaction.objects.select_related('customer', 'user').all()

    if query:
        interactions = interactions.filter(
            Q(subject__icontains=query) |
            Q(customer__full_name__icontains=query)
        )
    if type_filter:
        interactions = interactions.filter(type=type_filter)

    context = {
        'interactions': interactions,
        'query': query,
        'type_filter': type_filter,
        'total': interactions.count(),
    }
    return render(request, 'interactions/interaction_list.html', context)


@login_required
def interaction_add(request, customer_pk=None):
    customer = None
    customers = None
    if customer_pk:
        customer = get_object_or_404(Customer, pk=customer_pk)
    else:
        customers = Customer.objects.all().order_by('full_name')

    if request.method == 'POST':
        if not customer:
            customer_id = request.POST.get('customer')
            customer = get_object_or_404(Customer, pk=customer_id)

        Interaction.objects.create(
            customer=customer,
            user=request.user,
            type=request.POST.get('type'),
            subject=request.POST.get('subject'),
            description=request.POST.get('description', ''),
            direction=request.POST.get('direction', ''),
            duration_minutes=request.POST.get('duration_minutes') or None,
            outcome=request.POST.get('outcome', ''),
            interaction_date=request.POST.get('interaction_date'),
        )
        return redirect('customer_detail', pk=customer.pk)

    context = {'customer': customer}
    if customers is not None:
        context['customers'] = customers
    return render(request, 'interactions/interaction_add.html', context)


@login_required
def interaction_edit(request, pk):
    interaction = get_object_or_404(Interaction, pk=pk)
    if request.method == 'POST':
        interaction.type = request.POST.get('type')
        interaction.subject = request.POST.get('subject')
        interaction.description = request.POST.get('description', '')
        interaction.direction = request.POST.get('direction', '')
        interaction.duration_minutes = request.POST.get('duration_minutes') or None
        interaction.outcome = request.POST.get('outcome', '')
        interaction.interaction_date = request.POST.get('interaction_date')
        interaction.save()
        return redirect('customer_detail', pk=interaction.customer.pk)

    return render(request, 'interactions/interaction_edit.html', {'interaction': interaction})


@login_required
def interaction_delete(request, pk):
    interaction = get_object_or_404(Interaction, pk=pk)
    customer_pk = interaction.customer.pk
    if request.method == 'POST':
        interaction.delete()
        return redirect('customer_detail', pk=customer_pk)
    return render(request, 'interactions/interaction_confirm_delete.html', {'interaction': interaction})