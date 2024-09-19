from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('book-lesson/', views.book_lesson, name='book_lesson'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    # Remove the catch-all pattern that was here before
]