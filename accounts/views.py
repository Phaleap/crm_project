from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Role
from django.contrib.auth.models import Permission

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def role_list(request):
    """Display all roles"""
    roles = Role.objects.all()
    return render(request, 'accounts/role_list.html', {'roles': roles})

@login_required
def role_add(request):
    """Create a new role"""
    permissions = Permission.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        permission_ids = request.POST.getlist('permissions')
        
        role = Role.objects.create(name=name, description=description)
        if permission_ids:
            role.permissions.set(permission_ids)
        
        return redirect('role_list')
    
    return render(request, 'accounts/role_add.html', {'permissions': permissions})

@login_required
def role_edit(request, pk):
    """Edit a role"""
    role = get_object_or_404(Role, pk=pk)
    permissions = Permission.objects.all()
    
    if request.method == 'POST':
        role.name = request.POST.get('name')
        role.description = request.POST.get('description', '')
        role.save()
        
        permission_ids = request.POST.getlist('permissions')
        role.permissions.set(permission_ids)
        
        return redirect('role_list')
    
    return render(request, 'accounts/role_edit.html', {
        'role': role,
        'permissions': permissions
    })

@login_required
def role_delete(request, pk):
    """Delete a role"""
    role = get_object_or_404(Role, pk=pk)
    
    if request.method == 'POST':
        role.delete()
        return redirect('role_list')
    
    return render(request, 'accounts/role_confirm_delete.html', {'role': role})