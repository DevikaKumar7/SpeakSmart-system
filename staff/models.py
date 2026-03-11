from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class Batch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, related_name='students')
    enrolled_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


# ─── CLASS TIME SCHEDULING ────────────────────────────────────────────────────

class ClassSchedule(models.Model):
    DAY_CHOICES = [
        ('Monday',    'Monday'),
        ('Tuesday',   'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday',  'Thursday'),
        ('Friday',    'Friday'),
        ('Saturday',  'Saturday'),
        ('Sunday',    'Sunday'),
    ]

    STATUS_CHOICES = [
        ('scheduled',  'Scheduled'),
        ('ongoing',    'Ongoing'),
        ('completed',  'Completed'),
        ('cancelled',  'Cancelled'),
    ]

    SUBJECT_CHOICES = [
        ('reading',   'Reading'),
        ('writing',   'Writing'),
        ('listening', 'Listening'),
        ('speaking',  'Speaking'),
        ('general',   'General English'),
    ]

    title       = models.CharField(max_length=200)
    batch       = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='class_schedules')
    subject     = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    date        = models.DateField()
    day         = models.CharField(max_length=10, choices=DAY_CHOICES, blank=True)
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    venue       = models.CharField(max_length=100, blank=True)
    notes       = models.TextField(blank=True)
    status      = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} – {self.batch.name} ({self.date})"

    def duration_display(self):
        from datetime import datetime, date
        start = datetime.combine(date.today(), self.start_time)
        end   = datetime.combine(date.today(), self.end_time)
        diff  = end - start
        mins  = int(diff.total_seconds() / 60)
        h, m  = divmod(mins, 60)
        return f"{h}h {m}m" if h else f"{m}m"

    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def save(self, *args, **kwargs):
        # Auto-fill day of week from date
        if self.date:
            self.day = self.date.strftime('%A')
        self.full_clean()
        super().save(*args, **kwargs)