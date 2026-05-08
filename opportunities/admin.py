from django.contrib import admin
from .models import Opportunity

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'stage', 'value', 'probability', 'assigned_to']
    list_filter = ['stage']
    search_fields = ['title']