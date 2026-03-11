from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import StaffProfile, Student, Batch
from .forms import StaffRegistrationForm, StudentForm, BatchForm, ClassSchedule
from django.db.models import Q
from datetime import date


def staff_login(request):
    if request.user.is_authenticated:
        return redirect('staff:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('staff:dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a staff member.')
    return render(request, 'staff/login.html', {'role': 'Staff'})


def student_login(request):
    if request.user.is_authenticated:
        return redirect('staff:student_portal')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'student_profile'):
            login(request, user)
            return redirect('staff:student_portal')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'staff/login.html', {'role': 'Student'})

@login_required
def student_dashboard(request):
    """Full student dashboard with content counts and pending tasks."""
    if request.user.is_staff:
        return redirect('staff:dashboard')

    student = get_object_or_404(Student, user=request.user)

    # Content counts for the 4 skill cards
    content_counts = {
        'phrases':     Phrase.objects.filter(is_active=True).count(),
        'paragraphs':  Paragraph.objects.filter(is_active=True).count(),
        'vocabulary':  Vocabulary.objects.filter(is_active=True).count(),
        'prompts':     WritingPrompt.objects.filter(is_active=True).count(),
        'exercises':   WritingExercise.objects.filter(is_active=True).count(),
        'grammar':     GrammarRule.objects.filter(is_active=True).count(),
        'tracks':      ListeningTrack.objects.filter(is_active=True).count(),
        'dictations':  Dictation.objects.filter(is_active=True).count(),
        'topics':      SpeakingTopic.objects.filter(is_active=True).count(),
        'roleplay':    Roleplay.objects.filter(is_active=True).count(),
    }

    # Tasks for this student's batch
    assigned_tasks = TaskAssignment.objects.filter(
        batch=student.batch, is_active=True
    ).order_by('due_date') if student.batch else TaskAssignment.objects.none()

    submitted_ids = TaskSubmission.objects.filter(
        student=student
    ).values_list('task_id', flat=True)

    pending_tasks = assigned_tasks.exclude(id__in=submitted_ids)
    completed_tasks = assigned_tasks.filter(id__in=submitted_ids)

    return render(request, 'staff/student_dashboard.html', {
        'student':         student,
        'content_counts':  content_counts,
        'pending_tasks':   pending_tasks,
        'completed_tasks': completed_tasks,
        'total_assigned':  assigned_tasks.count(),
        'submitted_count': completed_tasks.count(),
    })


def staff_logout(request):
    logout(request)
    return redirect('staff:login')


def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff account created successfully!')
            return redirect('staff:login')
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff/register.html', {'form': form})


@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    total_students = Student.objects.filter(is_active=True).count()
    total_batches = Batch.objects.filter(is_active=True).count()
    recent_students = Student.objects.order_by('-enrolled_date')[:5]
    batches = Batch.objects.filter(is_active=True)
    return render(request, 'staff/dashboard.html', {
        'total_students': total_students,
        'total_batches': total_batches,
        'recent_students': recent_students,
        'batches': batches,
    })

@login_required
def schedule_list(request):
    """List all class schedules with filters."""
    if not request.user.is_staff:
        return redirect('staff:student_portal')

    batch_id   = request.GET.get('batch', '')
    status_f   = request.GET.get('status', '')
    subject_f  = request.GET.get('subject', '')
    date_f     = request.GET.get('date', '')
    search     = request.GET.get('search', '')

    schedules = ClassSchedule.objects.select_related('batch', 'created_by').all()

    if batch_id:
        schedules = schedules.filter(batch_id=batch_id)
    if status_f:
        schedules = schedules.filter(status=status_f)
    if subject_f:
        schedules = schedules.filter(subject=subject_f)
    if date_f:
        schedules = schedules.filter(date=date_f)
    if search:
        schedules = schedules.filter(
            Q(title__icontains=search) | Q(venue__icontains=search)
        )

    batches = Batch.objects.filter(is_active=True)
    return render(request, 'staff/schedule_list.html', {
        'schedules':   schedules,
        'batches':     batches,
        'batch_id':    batch_id,
        'status_f':    status_f,
        'subject_f':   subject_f,
        'date_f':      date_f,
        'search':      search,
        'today':       date.today(),
        'status_choices':  ClassSchedule.STATUS_CHOICES,
        'subject_choices': ClassSchedule.SUBJECT_CHOICES,
    })


@login_required
def student_portal(request):
    if request.user.is_staff:
        return redirect('staff:dashboard')
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'staff/student_portal.html', {'student': student})


@login_required
def batch_list(request):
    batches = Batch.objects.all().order_by('-created_at')
    return render(request, 'staff/batch_list.html', {'batches': batches})


@login_required
def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.created_by = request.user
            batch.save()
            messages.success(request, f'Batch "{batch.name}" created successfully!')
            return redirect('staff:batch_list')
    else:
        form = BatchForm()
    return render(request, 'staff/batch_form.html', {'form': form, 'title': 'Create Batch'})


@login_required
def batch_edit(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch updated successfully!')
            return redirect('staff:batch_list')
    else:
        form = BatchForm(instance=batch)
    return render(request, 'staff/batch_form.html', {'form': form, 'title': 'Edit Batch'})


@login_required
def student_list(request):
    batch_id = request.GET.get('batch')
    search = request.GET.get('search', '')
    students = Student.objects.select_related('batch').all()
    if batch_id:
        students = students.filter(batch_id=batch_id)
    if search:
        students = students.filter(
            first_name__icontains=search
        ) | students.filter(last_name__icontains=search) | students.filter(student_id__icontains=search)
    batches = Batch.objects.filter(is_active=True)
    return render(request, 'staff/student_list.html', {
        'students': students.order_by('batch__name', 'first_name'),
        'batches': batches,
        'selected_batch': batch_id,
        'search': search,
    })


@login_required
def student_create(request):
    batch_id = request.GET.get('batch')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Create user account
            username = student.email.split('@')[0]
            password = form.cleaned_data.get('password') or User.objects.make_random_password()
            user = User.objects.create_user(
                username=username,
                email=student.email,
                password=password,
                first_name=student.first_name,
                last_name=student.last_name,
            )
            student.user = user
            student.save()
            messages.success(request, f'Student "{student.get_full_name()}" added! Login: {username}')
            return redirect('staff:student_list')
    else:
        initial = {}
        if batch_id:
            initial['batch'] = batch_id
        form = StudentForm(initial=initial)
    return render(request, 'staff/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'staff/student_detail.html', {'student': student})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('staff:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'staff/student_form.html', {'form': form, 'title': 'Edit Student'})


@login_required
def student_toggle(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.is_active = not student.is_active
    student.save()
    status = 'activated' if student.is_active else 'deactivated'
    messages.success(request, f'Student {status} successfully!')
    return redirect('staff:student_list')


@login_required
def batch_students(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    students = Student.objects.filter(batch=batch).order_by('first_name')
    return render(request, 'staff/batch_students.html', {'batch': batch, 'students': students})
