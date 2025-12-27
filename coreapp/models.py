from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Role choices
class Role(models.TextChoices):
    STUDENT = 'student', 'Student'
    TEACHER = 'teacher', 'Teacher'
    DEPARTMENT_HEAD = 'department_head', 'Department Head'

class UserProfile(models.Model):
    """Extended user profile with role information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="User's role in the system"
    )
    department = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True, help_text="For students")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def is_student(self):
        return self.role == Role.STUDENT

    def is_teacher(self):
        return self.role == Role.TEACHER

    def is_department_head(self):
        return self.role == Role.DEPARTMENT_HEAD

# Signal to create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
