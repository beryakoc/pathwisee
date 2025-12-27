from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('role', 'department', 'student_id')

class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    list_display = ('user', 'role', 'department', 'student_id', 'created_at')
    list_filter = ('role', 'department', 'created_at')
    search_fields = ('user__username', 'user__email', 'student_id', 'department')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Additional Information', {
            'fields': ('department', 'student_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
