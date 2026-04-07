from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date
import csv
import io
import secrets
import string
from django.http import HttpResponse

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


# ─── ADD THESE TWO VIEWS anywhere in staff/views.py ──────────────────────────
 
@login_required
def student_bulk_import(request):
    """Import multiple students from a CSV file."""
    if not request.user.is_staff:
        return redirect('staff:student_portal')
 
    batches = Batch.objects.filter(is_active=True)
    results = None
 
    if request.method == 'POST':
        csv_file      = request.FILES.get('csv_file')
        default_batch_id = request.POST.get('default_batch')
        skip_dupes    = 'skip_duplicates' in request.POST
        auto_password = 'auto_password'   in request.POST
 
        if not csv_file:
            messages.error(request, 'Please upload a CSV file.')
            return render(request, 'staff/student_bulk_import.html', {'batches': batches})
 
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File must be a .csv file.')
            return render(request, 'staff/student_bulk_import.html', {'batches': batches})
 
        try:
            default_batch = Batch.objects.get(pk=default_batch_id) if default_batch_id else None
        except Batch.DoesNotExist:
            default_batch = None
 
        # Decode file
        try:
            decoded = csv_file.read().decode('utf-8-sig')  # utf-8-sig handles BOM
        except UnicodeDecodeError:
            decoded = csv_file.read().decode('latin-1')
 
        reader = csv.DictReader(io.StringIO(decoded))
 
        # Normalise headers (lowercase + strip)
        reader.fieldnames = [h.strip().lower() for h in (reader.fieldnames or [])]
 
        created          = 0
        skipped          = 0
        errors           = []
        skipped_details  = []
        total            = 0
 
        REQUIRED = {'student_id', 'first_name', 'last_name', 'email'}
        missing  = REQUIRED - set(reader.fieldnames)
        if missing:
            messages.error(request, f'CSV is missing required columns: {", ".join(missing)}')
            return render(request, 'staff/student_bulk_import.html', {'batches': batches})
 
        for row_num, row in enumerate(reader, start=2):  # start=2 (row 1 = header)
            total += 1
            # Clean values
            row = {k: (v.strip() if v else '') for k, v in row.items()}
 
            student_id = row.get('student_id', '')
            first_name = row.get('first_name', '')
            last_name  = row.get('last_name',  '')
            email      = row.get('email',      '')
 
            # Validate required fields
            if not all([student_id, first_name, last_name, email]):
                errors.append({'row': row_num, 'message': f'Missing required field(s) — student_id={student_id}, email={email}'})
                continue
 
            # Basic email validation
            if '@' not in email:
                errors.append({'row': row_num, 'message': f'Invalid email address: {email}'})
                continue
 
            # Check duplicates
            if skip_dupes:
                if Student.objects.filter(student_id=student_id).exists():
                    skipped += 1
                    skipped_details.append(f'Row {row_num}: student_id "{student_id}" already exists')
                    continue
                if Student.objects.filter(email=email).exists():
                    skipped += 1
                    skipped_details.append(f'Row {row_num}: email "{email}" already exists')
                    continue
                if User.objects.filter(email=email).exists():
                    skipped += 1
                    skipped_details.append(f'Row {row_num}: user with email "{email}" already exists')
                    continue
 
            # Resolve batch
            batch = default_batch
            batch_name = row.get('batch', '').strip()
            if batch_name:
                resolved = Batch.objects.filter(name__iexact=batch_name).first()
                if resolved:
                    batch = resolved
 
            # Gender
            gender = row.get('gender', '').upper()
            if gender not in ('M', 'F', 'O'):
                gender = ''
 
            # Date of birth
            from datetime import datetime
            dob = None
            dob_str = row.get('date_of_birth', '')
            if dob_str:
                for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y'):
                    try:
                        dob = datetime.strptime(dob_str, fmt).date()
                        break
                    except ValueError:
                        continue
 
            # Password
            password = row.get('password', '').strip()
            if not password or auto_password:
                alphabet = string.ascii_letters + string.digits + '!@#$'
                password = ''.join(secrets.choice(alphabet) for _ in range(12))
 
            # Username = email prefix
            username = email.split('@')[0]
            # Ensure unique username
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
 
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                Student.objects.create(
                    user=user,
                    student_id=student_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=row.get('phone', ''),
                    gender=gender,
                    date_of_birth=dob,
                    batch=batch,
                )
                created += 1
            except Exception as e:
                # Rollback user if student creation failed
                try:
                    User.objects.filter(username=username).delete()
                except Exception:
                    pass
                errors.append({'row': row_num, 'message': str(e)})
 
        results = {
            'created':         created,
            'skipped':         skipped,
            'errors':          errors,
            'skipped_details': skipped_details,
            'total':           total,
        }
 
        if created:
            messages.success(request, f'✅ {created} student(s) imported successfully!')
        if skipped:
            messages.warning(request, f'⚠️ {skipped} row(s) skipped (duplicates).')
        if errors:
            messages.error(request, f'❌ {len(errors)} row(s) had errors.')
 
    return render(request, 'staff/student_bulk_import.html', {
        'batches': batches,
        'results': results,
    })
 
 
@login_required
def student_csv_template(request):
    """Download a blank CSV template for bulk student import."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_import_template.csv"'
 
    writer = csv.writer(response)
    # Header row
    writer.writerow([
        'student_id', 'first_name', 'last_name', 'email',
        'phone', 'gender', 'date_of_birth', 'batch', 'password'
    ])
    # Sample rows
    writer.writerow(['STU001', 'John',  'Smith', 'john@example.com',  '9876543210', 'M', '2000-06-15', 'Batch A', ''])
    writer.writerow(['STU002', 'Jane',  'Doe',   'jane@example.com',  '9123456789', 'F', '2001-03-22', 'Batch B', ''])
    writer.writerow(['STU003', 'Alex',  'Kumar', 'alex@example.com',  '',           '',  '',           'Batch A', ''])
 
    return response


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
            alphabet = string.ascii_letters + string.digits + '!@#$'
            password = form.cleaned_data.get('password') or ''.join(secrets.choice(alphabet) for _ in range(12))
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