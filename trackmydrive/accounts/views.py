from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, StudentProfileForm, InstructorProfileForm
from core.models import Student, Instructor

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'student':
                Student.objects.create(user=user)
            elif user_type == 'instructor':
                Instructor.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful. Please complete your profile.')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    
    # Check if the user has a profile
    if hasattr(user, 'student'):
        return student_profile(request)
    elif hasattr(user, 'instructor'):
        return instructor_profile(request)
    else:
        # If no profile exists, create a student profile by default
        Student.objects.create(user=user)
        messages.info(request, "A student profile has been created for you. Please update your information.")
        return redirect('student_profile')

@login_required
def student_profile(request):
    student, created = Student.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "A new student profile has been created for you. Please update your information.")
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'accounts/student_profile.html', {'form': form})

@login_required
def instructor_profile(request):
    instructor, created = Instructor.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "A new instructor profile has been created for you. Please update your information.")
    
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = InstructorProfileForm(instance=instructor)
    return render(request, 'accounts/instructor_profile.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')