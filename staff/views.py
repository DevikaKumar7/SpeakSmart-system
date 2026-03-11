from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date

from .models import StaffProfile, Student, Batch, ClassSchedule
from .forms import StaffRegistrationForm, StudentForm, BatchForm, ClassScheduleForm


# ─── AUTH ─────────────────────────────────────────────────────────────────────

def staff_login(request):
    if request.user.is_authenticated:
        return redirect('staff:dashboard') if request.user.is_staff else redirect('staff:student_portal')
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user and user.is_staff:
            login(request, user)
            return redirect('staff:dashboard')
        messages.error(request, 'Invalid credentials or not a staff member.')
    return render(request, 'staff/login.html', {'role': 'Staff'})


def student_login(request):
    if request.user.is_authenticated:
        return redirect('staff:dashboard') if request.user.is_staff else redirect('staff:student_portal')
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user and hasattr(user, 'student_profile'):
            login(request, user)
            return redirect('staff:student_portal')
        messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'staff/login.html', {'role': 'Student'})


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


# ─── STAFF DASHBOARD ──────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    today          = date.today()
    total_students = Student.objects.filter(is_active=True).count()
    total_batches  = Batch.objects.filter(is_active=True).count()
    recent_students = Student.objects.order_by('-enrolled_date')[:5]
    batches         = Batch.objects.filter(is_active=True)
    today_classes   = ClassSchedule.objects.filter(date=today).select_related('batch').order_by('start_time')
    upcoming        = ClassSchedule.objects.filter(date__gt=today, status='scheduled') \
                                           .select_related('batch').order_by('date', 'start_time')[:5]
    return render(request, 'staff/dashboard.html', {
        'total_students':  total_students,
        'total_batches':   total_batches,
        'recent_students': recent_students,
        'batches':         batches,
        'today_classes':   today_classes,
        'upcoming_classes': upcoming,
        'today':           today,
    })


# ─── STUDENT PORTAL ───────────────────────────────────────────────────────────

@login_required
def student_portal(request):
    if request.user.is_staff:
        return redirect('staff:dashboard')
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'staff/student_portal.html', {'student': student})


# ─── BATCH ────────────────────────────────────────────────────────────────────

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
def batch_students(request, pk):
    batch    = get_object_or_404(Batch, pk=pk)
    students = Student.objects.filter(batch=batch).order_by('first_name')
    return render(request, 'staff/batch_students.html', {'batch': batch, 'students': students})


# ─── STUDENT ──────────────────────────────────────────────────────────────────

@login_required
def student_list(request):
    batch_id = request.GET.get('batch')
    search   = request.GET.get('search', '')
    students = Student.objects.select_related('batch').all()
    if batch_id:
        students = students.filter(batch_id=batch_id)
    if search:
        students = (students.filter(first_name__icontains=search) |
                    students.filter(last_name__icontains=search)   |
                    students.filter(student_id__icontains=search))
    batches = Batch.objects.filter(is_active=True)
    return render(request, 'staff/student_list.html', {
        'students':       students.order_by('batch__name', 'first_name'),
        'batches':        batches,
        'selected_batch': batch_id,
        'search':         search,
    })


@login_required
def student_create(request):
    batch_id = request.GET.get('batch')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student  = form.save(commit=False)
            username = student.email.split('@')[0]
            password = form.cleaned_data.get('password') or User.objects.make_random_password()
            user = User.objects.create_user(
                username=username, email=student.email, password=password,
                first_name=student.first_name, last_name=student.last_name,
            )
            student.user = user
            student.save()
            messages.success(request, f'Student "{student.get_full_name()}" added! Login: {username}')
            return redirect('staff:student_list')
    else:
        form = StudentForm(initial={'batch': batch_id} if batch_id else {})
    return render(request, 'staff/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_detail(request, pk):
    return render(request, 'staff/student_detail.html',
                  {'student': get_object_or_404(Student, pk=pk)})


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
    messages.success(request, f'Student {"activated" if student.is_active else "deactivated"} successfully!')
    return redirect('staff:student_list')


# ─── CLASS TIME SCHEDULING ────────────────────────────────────────────────────

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
def schedule_create(request):
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.created_by = request.user
            schedule.save()
            messages.success(request, f'Class "{schedule.title}" scheduled successfully!')
            return redirect('staff:schedule_list')
    else:
        # Pre-fill batch if passed via query string
        initial = {}
        if request.GET.get('batch'):
            initial['batch'] = request.GET.get('batch')
        form = ClassScheduleForm(initial=initial)
    return render(request, 'staff/schedule_form.html', {
        'form':  form,
        'title': 'Schedule New Class',
    })


@login_required
def schedule_detail(request, pk):
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    return render(request, 'staff/schedule_detail.html', {'schedule': schedule})


@login_required
def schedule_edit(request, pk):
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated successfully!')
            return redirect('staff:schedule_list')
    else:
        form = ClassScheduleForm(instance=schedule)
    return render(request, 'staff/schedule_form.html', {
        'form':     form,
        'title':    'Edit Class Schedule',
        'schedule': schedule,
    })


@login_required
def schedule_delete(request, pk):
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        title = schedule.title
        schedule.delete()
        messages.success(request, f'Schedule "{title}" deleted.')
        return redirect('staff:schedule_list')
    return render(request, 'staff/schedule_confirm_delete.html', {'schedule': schedule})


@login_required
def schedule_status_update(request, pk):
    """Quick status change via POST."""
    if not request.user.is_staff:
        return redirect('staff:student_portal')
    schedule = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = [s[0] for s in ClassSchedule.STATUS_CHOICES]
        if new_status in valid:
            schedule.status = new_status
            schedule.save()
            messages.success(request, f'Status updated to "{schedule.get_status_display()}".')
    return redirect('staff:schedule_list')


@login_required
def schedule_timetable(request):
    """Weekly timetable view grouped by batch."""
    if not request.user.is_staff:
        return redirect('staff:student_portal')

    batch_id = request.GET.get('batch', '')
    batches  = Batch.objects.filter(is_active=True)

    schedules = ClassSchedule.objects.select_related('batch').filter(
        status__in=['scheduled', 'ongoing']
    )
    if batch_id:
        schedules = schedules.filter(batch_id=batch_id)

    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timetable = {day: [] for day in DAYS}
    for s in schedules:
        if s.day in timetable:
            timetable[s.day].append(s)

    return render(request, 'staff/schedule_timetable.html', {
        'timetable': timetable,
        'days':      DAYS,
        'batches':   batches,
        'batch_id':  batch_id,
    })