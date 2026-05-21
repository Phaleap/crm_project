from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Role

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def role_list(request):
    roles = Role.objects.all()
    return render(request, 'role/role_list.html', {'roles': roles})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def role_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        permissions = request.POST.getlist('permissions')

        role = Role.objects.create(
            name=name,
            description=description,
        )
        if permissions:
            role.permissions.set(permissions)
        messages.success(request, 'Role created successfully.')
        return redirect('role_list')
    from django.contrib.auth.models import Permission
    permissions = Permission.objects.all().order_by('content_type__app_label', 'codename')
    return render(request, 'role/role_add.html', {'permissions': permissions})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.name = request.POST.get('name')
        role.description = request.POST.get('description')
        permissions = request.POST.getlist('permissions')
        role.permissions.set(permissions)
        role.save()
        messages.success(request, 'Role updated successfully.')
        return redirect('role_list')
    from django.contrib.auth.models import Permission
    permissions = Permission.objects.all().order_by('content_type__app_label', 'codename')
    return render(request, 'role/role_edit.html', {'role': role, 'permissions': permissions})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully.')
        return redirect('role_list')
    return render(request, 'role/role_confirm_delete.html', {'role': role})

def PostAPICategory(request):
    return render(request, 'PostAPICategory.html')