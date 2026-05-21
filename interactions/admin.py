from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'type', 'subject', 'direction', 'outcome', 'interaction_date', 'user']
    list_filter = ['type', 'direction', 'outcome']
    search_fields = ['subject', 'customer__full_name']