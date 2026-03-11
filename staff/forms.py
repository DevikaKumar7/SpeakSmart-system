from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StaffProfile, Student, Batch, ClassSchedule


class StaffRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    employee_id = forms.CharField(max_length=20, required=True)
    phone = forms.CharField(max_length=15, required=False)
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = True
        if commit:
            user.save()
            StaffProfile.objects.create(
                user=user,
                employee_id=self.cleaned_data['employee_id'],
                phone=self.cleaned_data.get('phone', ''),
                department=self.cleaned_data.get('department', ''),
            )
        return user


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False,
                                help_text="Leave blank to auto-generate")

    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'phone',
                  'gender', 'date_of_birth', 'batch']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# ─── CLASS TIME SCHEDULE FORM ─────────────────────────────────────────────────

class ClassScheduleForm(forms.ModelForm):

    class Meta:
        model  = ClassSchedule
        fields = [
            'title', 'batch', 'subject',
            'date', 'start_time', 'end_time',
            'venue', 'notes', 'status',
        ]
        widgets = {
            'date':       forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time':   forms.TimeInput(attrs={'type': 'time'}),
            'notes':      forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any additional notes…'}),
            'venue':      forms.TextInput(attrs={'placeholder': 'e.g. Room 101, Online – Zoom'}),
            'title':      forms.TextInput(attrs={'placeholder': 'e.g. Speaking Practice – Week 3'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end   = cleaned.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned        
