from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Role

def role_required(*allowed_roles):
    """
    Decorator to check if user has one of the required roles.
    Usage: @role_required(Role.TEACHER, Role.DEPARTMENT_HEAD)
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('admin:login')
            
            # Check if user has a profile
            if not hasattr(request.user, 'profile'):
                # Create a default profile if it doesn't exist
                from .models import UserProfile
                UserProfile.objects.get_or_create(
                    user=request.user,
                    defaults={'role': Role.STUDENT}
                )
            
            user_role = request.user.profile.role
            
            if user_role not in allowed_roles:
                raise PermissionDenied("You don't have permission to access this page.")
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

def student_required(view_func):
    """Decorator to require student role"""
    return role_required(Role.STUDENT)(view_func)

def teacher_required(view_func):
    """Decorator to require teacher role"""
    return role_required(Role.TEACHER)(view_func)

def department_head_required(view_func):
    """Decorator to require department head role"""
    return role_required(Role.DEPARTMENT_HEAD)(view_func)

def teacher_or_department_head_required(view_func):
    """Decorator to require teacher or department head role"""
    return role_required(Role.TEACHER, Role.DEPARTMENT_HEAD)(view_func)

