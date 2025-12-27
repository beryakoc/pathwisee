from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # Disabled - redirects to login
    path('courses/', views.courses, name='courses'),
    path('announcements/', views.announcements, name='announcements'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('students/', views.students, name='students'),
    path('overview/', views.overview, name='overview'),
    path('management/', views.management, name='management'),
    path('management/users/', views.user_management, name='user_management'),
    path('management/users/create/', views.create_user, name='create_user'),
]

