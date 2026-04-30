from django.contrib import admin
from .models import Customer, CustomerTag

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company', 'segment', 'status', 'assigned_to']
    list_filter = ['status', 'segment']
    search_fields = ['full_name', 'email', 'company']

@admin.register(CustomerTag)
class CustomerTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']