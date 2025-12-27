from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Role, UserProfile

class UserCreationByAdminForm(UserCreationForm):
    """Form for Department Head to create Student or Teacher accounts"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Email address'
    }))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Last name'
    }))
    role = forms.ChoiceField(
        choices=[(Role.STUDENT, 'Student'), (Role.TEACHER, 'Teacher')],
        initial=Role.STUDENT,
        widget=forms.Select(attrs={
            'class': 'form-input'
        }),
        help_text="Department Head role cannot be assigned through this form"
    )
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Department (optional)'
    }))
    student_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Student ID (optional, for students)'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'department', 'student_id')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm password'
        })

    def clean_role(self):
        """Prevent Department Head role assignment"""
        role = self.cleaned_data.get('role')
        if role == Role.DEPARTMENT_HEAD:
            raise forms.ValidationError("Department Head role cannot be assigned through user creation.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create profile with role
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': self.cleaned_data['role'],
                    'department': self.cleaned_data['department'] or '',
                    'student_id': self.cleaned_data['student_id'] or ''
                }
            )
            if not created:
                profile.role = self.cleaned_data['role']
                profile.department = self.cleaned_data['department'] or ''
                profile.student_id = self.cleaned_data['student_id'] or ''
                profile.save()
        return user

class RegistrationForm(UserCreationForm):
    """Registration form with role selection"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Email address'
    }))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Last name'
    }))
    role = forms.ChoiceField(
        choices=Role.choices,
        initial=Role.STUDENT,
        widget=forms.Select(attrs={
            'class': 'form-input'
        })
    )
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Department (optional)'
    }))
    student_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Student ID (optional)'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'department', 'student_id')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create or update profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': self.cleaned_data['role'],
                    'department': self.cleaned_data['department'] or '',
                    'student_id': self.cleaned_data['student_id'] or ''
                }
            )
            if not created:
                profile.role = self.cleaned_data['role']
                profile.department = self.cleaned_data['department'] or ''
                profile.student_id = self.cleaned_data['student_id'] or ''
                profile.save()
        return user

