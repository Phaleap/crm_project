from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from rest_framework.permissions import BasePermission


ADMIN = 'admin'
SALES = 'sales_staff'
SERVICE = 'customer_service'


def has_role(user, *roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser or getattr(user, 'role', None) == ADMIN:
        return True
    return getattr(user, 'role', None) in roles


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if has_role(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access that CRM module.')
            return redirect('dashboard')
        return wrapper
    return decorator


admin_required = role_required(ADMIN)
sales_required = role_required(SALES)
service_required = role_required(SERVICE)
sales_or_service_required = role_required(SALES, SERVICE)


class RolePermission(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return has_role(request.user, *self.allowed_roles)


class IsAdminRole(RolePermission):
    allowed_roles = (ADMIN,)


class IsSalesRole(RolePermission):
    allowed_roles = (SALES,)


class IsServiceRole(RolePermission):
    allowed_roles = (SERVICE,)


class IsSalesOrServiceRole(RolePermission):
    allowed_roles = (SALES, SERVICE)
