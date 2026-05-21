from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    filter_horizontal = ['permissions']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'user_role', 'is_active']
    list_filter = ['role', 'user_role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('CRM Info', {'fields': ('role', 'phone', 'profile_image', 'user_role')}),
    )