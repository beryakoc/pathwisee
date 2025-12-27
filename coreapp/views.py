from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import UserCreationByAdminForm
from .decorators import (
    student_required,
    teacher_required,
    department_head_required,
    teacher_or_department_head_required
)

def home(request):
    """Home page view - accessible to all authenticated users"""
    return render(request, 'home.html')

@login_required
def courses(request):
    """Courses page view - accessible to all authenticated users"""
    return render(request, 'courses.html')

@login_required
def announcements(request):
    """Announcements page view - accessible to all authenticated users"""
    return render(request, 'announcements.html')

@login_required
def profile(request):
    """Profile page view - accessible to all authenticated users"""
    return render(request, 'profile.html')

@teacher_required
def students(request):
    """Students page view - only for teachers"""
    return render(request, 'students.html')

@student_required
def overview(request):
    """Overview page view - only for students"""
    return render(request, 'overview.html')

@department_head_required
def management(request):
    """Management page view - only for department head"""
    return render(request, 'management.html')

@department_head_required
def user_management(request):
    """User management page - list all users (Department Head only)"""
    users_list = User.objects.select_related('profile').all().order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users_list, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'user_management.html', {'users': users})

@department_head_required
def create_user(request):
    """Create new user - Department Head only"""
    if request.method == 'POST':
        form = UserCreationByAdminForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            role_display = form.cleaned_data.get('role')
            messages.success(request, f'User "{username}" created successfully as {role_display}.')
            return redirect('user_management')
    else:
        form = UserCreationByAdminForm()
    
    return render(request, 'create_user.html', {'form': form})

@login_required
def change_password(request):
    """Password change view - accessible to all authenticated users"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

def register(request):
    """Public registration - DISABLED"""
    messages.error(request, 'Public registration is disabled. Please contact your Department Head to create an account.')
    return redirect('admin:login')
