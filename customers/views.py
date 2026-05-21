from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Customer


@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    segment = request.GET.get('segment', '')

    customers = Customer.objects.all().order_by('-created_at')

    if query:
        customers = customers.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )
    if status:
        customers = customers.filter(status=status)
    if segment:
        customers = customers.filter(segment=segment)

    context = {
        'customers': customers,
        'query': query,
        'status': status,
        'segment': segment,
        'total': customers.count(),
    }
    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    interactions = customer.interactions.select_related('user').order_by('-interaction_date')
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'interactions': interactions,
    })


@login_required
def customer_add(request):
    if request.method == 'POST':
        Customer.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email') or None,
            phone=request.POST.get('phone'),
            company=request.POST.get('company'),
            job_title=request.POST.get('job_title'),
            segment=request.POST.get('segment'),
            industry=request.POST.get('industry'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            status=request.POST.get('status', 'active'),
            assigned_to=request.user,
            created_by=request.user,
        )
        return redirect('customer_list')
    return render(request, 'customers/customer_add.html')


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.full_name = request.POST.get('full_name')
        customer.email = request.POST.get('email') or None
        customer.phone = request.POST.get('phone')
        customer.company = request.POST.get('company')
        customer.job_title = request.POST.get('job_title')
        customer.segment = request.POST.get('segment')
        customer.industry = request.POST.get('industry')
        customer.city = request.POST.get('city')
        customer.country = request.POST.get('country')
        customer.status = request.POST.get('status', 'active')
        customer.save()
        return redirect('customer_detail', pk=pk)
    return render(request, 'customers/customer_edit.html', {'customer': customer})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})