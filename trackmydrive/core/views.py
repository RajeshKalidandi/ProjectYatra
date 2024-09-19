from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Lesson, Student, Instructor
from .forms import LessonForm
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Create your views here.
def health_check(request):
    return JsonResponse({"status": "ok"})

def home(request):
    return render(request, 'core/home.html')

@login_required
def book_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.student = request.user.student
            lesson.save()
            messages.success(request, 'Lesson booked successfully!')
            return redirect('lesson_list')
    else:
        form = LessonForm()
    return render(request, 'core/book_lesson.html', {'form': form})

@login_required
def lesson_list(request):
    if hasattr(request.user, 'student'):
        lessons = request.user.student.lessons.all()
    elif hasattr(request.user, 'instructor'):
        lessons = request.user.instructor.lessons.all()
    else:
        lessons = []
    return render(request, 'core/lesson_list.html', {'lessons': lessons})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user.student != lesson.student and request.user.instructor != lesson.instructor:
        messages.error(request, "You don't have permission to view this lesson.")
        return redirect('lesson_list')
    return render(request, 'core/lesson_detail.html', {'lesson': lesson})

# Serve React App
index = never_cache(TemplateView.as_view(template_name='index.html'))
