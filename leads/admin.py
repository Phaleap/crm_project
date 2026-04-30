from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'source', 'status', 'rating', 'assigned_to']
    list_filter = ['status', 'rating', 'source']
    search_fields = ['full_name', 'email', 'company']