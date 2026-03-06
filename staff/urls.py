from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('login/', views.staff_login, name='login'),
    path('student-login/', views.student_login, name='student_login'),
    path('logout/', views.staff_logout, name='logout'),
    path('register/', views.staff_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student-portal/', views.student_portal, name='student_portal'),

    # Batch URLs
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/create/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/edit/', views.batch_edit, name='batch_edit'),
    path('batches/<int:pk>/students/', views.batch_students, name='batch_students'),

    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/toggle/', views.student_toggle, name='student_toggle'),
]
