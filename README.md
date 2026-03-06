# 📚 English Course Schedule System

A Django-based web application with two modules:
- **Staff Module** — staff/student management
- **English Scheduling Module** — activity content management (Reading, Writing, Listening, Speaking)

---

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations staff scheduling
python manage.py migrate
```

### 3. Create Superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### 4. Start the Development Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
english_course/
├── english_course/        # Project settings & main URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── staff/                 # Staff Module
│   ├── models.py          # StaffProfile, Batch, Student
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/staff/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── batch_list.html / batch_form.html / batch_students.html
│       ├── student_list.html / student_form.html / student_detail.html
│       └── student_portal.html
│
├── scheduling/            # English Scheduling Module
│   ├── models.py          # All activity models
│   ├── views.py           # CRUD views for all activities
│   ├── forms.py
│   ├── urls.py
│   └── templates/scheduling/
│       ├── dashboard.html
│       ├── confirm_delete.html
│       ├── reading/       # phrases, paragraphs, vocabulary
│       ├── writing/       # prompts, exercises, grammar
│       ├── listening/     # tracks, exercises, dictation
│       └── speaking/      # topics, pronunciation, roleplay
│
├── templates/
│   └── base.html          # Shared layout & sidebar navigation
│
├── manage.py
└── requirements.txt
```

---

## 🔐 User Roles

### Staff Login
- URL: `/staff/login/`
- Register: `/staff/register/`
- Access: Full system access (dashboard, batches, students, all scheduling)

### Student Login
- URL: `/staff/student-login/`
- Access: View-only student portal with all scheduling content

---

## 📋 Features

### Staff Module
| Feature | URL |
|---|---|
| Staff Register | `/staff/register/` |
| Staff Login | `/staff/login/` |
| Student Login | `/staff/student-login/` |
| Dashboard | `/staff/dashboard/` |
| Batch List | `/staff/batches/` |
| Create Batch | `/staff/batches/create/` |
| Students by Batch | `/staff/batches/<id>/students/` |
| Student List | `/staff/students/` |
| Add Student | `/staff/students/create/` |
| Student Detail | `/staff/students/<id>/` |

### English Scheduling Module

#### 📖 Reading
- **Phrases** — `/scheduling/reading/phrases/`
- **Paragraphs** — `/scheduling/reading/paragraphs/`
- **Vocabulary** — `/scheduling/reading/vocabulary/`

#### ✍️ Writing
- **Prompts** — `/scheduling/writing/prompts/`
- **Exercises** — `/scheduling/writing/exercises/`
- **Grammar Rules** — `/scheduling/writing/grammar/`

#### 🎧 Listening
- **Tracks** — `/scheduling/listening/tracks/`
- **Exercises** — `/scheduling/listening/exercises/`
- **Dictation** — `/scheduling/listening/dictation/`

#### 🗣️ Speaking
- **Topics** — `/scheduling/speaking/topics/`
- **Pronunciation** — `/scheduling/speaking/pronunciation/`
- **Roleplay** — `/scheduling/speaking/roleplay/`

Each activity supports: **List → Detail → Create → Edit → Delete → Enable/Disable**

---

## 🗃️ Database

Uses SQLite by default (`db.sqlite3`). To switch to PostgreSQL, update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
