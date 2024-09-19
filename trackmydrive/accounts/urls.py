from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/student/', views.student_profile, name='student_profile'),
    path('profile/instructor/', views.instructor_profile, name='instructor_profile'),
]