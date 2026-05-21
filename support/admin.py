from django.contrib import admin
from .models import SupportTicket, TicketComment


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    readonly_fields = ['author', 'created_at']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'subject', 'customer', 'issue_type', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'issue_type']
    search_fields = ['ticket_number', 'subject', 'customer__name']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']
    inlines = [TicketCommentInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at']