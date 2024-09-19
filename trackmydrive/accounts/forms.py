from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Student, Instructor

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=[('student', 'Student'), ('instructor', 'Instructor')])
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "user_type", "date_of_birth")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'phone_number', 'address', 'learner_permit_number', 'emergency_contact_name', 'emergency_contact_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['phone_number', 'address', 'license_number', 'years_of_experience', 'specializations']