from .models import Role

def user_role(request):
    """
    Context processor to make user role information available in all templates
    """
    context = {
        'user_role': None,
        'is_student': False,
        'is_teacher': False,
        'is_department_head': False,
    }
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            context['user_role'] = profile.role
            context['is_student'] = profile.is_student()
            context['is_teacher'] = profile.is_teacher()
            context['is_department_head'] = profile.is_department_head()
    
    return context

