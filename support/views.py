from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.permissions import service_required
from .models import SupportTicket, TicketComment
from .forms import SupportTicketForm, TicketCommentForm


@login_required
@service_required
def ticket_list(request):
    tickets = SupportTicket.objects.select_related('customer', 'assigned_to')

    status = request.GET.get('status')
    if status:
        tickets = tickets.filter(status=status)

    priority = request.GET.get('priority')
    if priority:
        tickets = tickets.filter(priority=priority)

    issue_type = request.GET.get('issue_type')
    if issue_type:
        tickets = tickets.filter(issue_type=issue_type)

    query = request.GET.get('q')
    if query:
        tickets = tickets.filter(
            Q(subject__icontains=query) |
            Q(ticket_number__icontains=query) |
            Q(customer__full_name__icontains=query)
        )

    context = {
        'tickets': tickets,
        'status_filter': status,
        'priority_filter': priority,
        'issue_type_filter': issue_type,
        'query': query,
        'total': tickets.count(),
        'open_count': SupportTicket.objects.filter(status='open').count(),
        'in_progress_count': SupportTicket.objects.filter(status='in_progress').count(),
        'resolved_count': SupportTicket.objects.filter(status='resolved').count(),
        'urgent_count': SupportTicket.objects.filter(priority='urgent').count(),
    }
    return render(request, 'support/ticket_list.html', context)


@login_required
@service_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    comments = ticket.comments.select_related('author')
    comment_form = TicketCommentForm()

    if request.method == 'POST':
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('ticket_detail', pk=pk)

    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'support/ticket_detail.html', context)


@login_required
@service_required
def ticket_add(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, f'Ticket {ticket.ticket_number} created successfully.')
            return redirect('ticket_list')
    else:
        form = SupportTicketForm()
    return render(request, 'support/ticket_form.html', {'form': form, 'action': 'Add'})


@login_required
@service_required
def ticket_edit(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket updated successfully.')
            return redirect('ticket_detail', pk=pk)
    else:
        form = SupportTicketForm(instance=ticket)
    return render(request, 'support/ticket_form.html', {'form': form, 'action': 'Edit', 'ticket': ticket})


@login_required
@service_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully.')
        return redirect('ticket_list')
    return render(request, 'support/ticket_confirm_delete.html', {'ticket': ticket})


@login_required
@service_required
def ticket_update_status(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(SupportTicket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()
            messages.success(request, f'Ticket status updated to {ticket.get_status_display()}.')
    return redirect('ticket_detail', pk=pk)
