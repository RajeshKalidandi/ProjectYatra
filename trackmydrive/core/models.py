from django.db import models
from django.contrib.auth.models import User

class DrivingSchool(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    learner_permit_number = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(DrivingSchool, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    license_number = models.CharField(max_length=20, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    specializations = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='lessons')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lesson with {self.instructor} for {self.student} on {self.start_time}"
