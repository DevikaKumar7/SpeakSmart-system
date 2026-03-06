from django.contrib import admin
from .models import StaffProfile, Student, Batch

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department']

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'is_active', 'student_count']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_full_name', 'batch', 'email', 'is_active']
    list_filter = ['batch', 'is_active']
    search_fields = ['first_name', 'last_name', 'student_id', 'email']
