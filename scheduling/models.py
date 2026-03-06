from django.db import models
from django.contrib.auth.models import User
from staff.models import Batch, Student

DIFFICULTY_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]


class Schedule(models.Model):
    title = models.CharField(max_length=200)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='schedules')
    description = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.batch.name}"


# ─── READING ───────────────────────────────────────────────────────────────────

class Phrase(models.Model):
    text = models.CharField(max_length=500)
    meaning = models.TextField()
    example_sentence = models.TextField(blank=True)
    translation = models.CharField(max_length=500, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    category = models.CharField(max_length=100, blank=True)
    audio_note = models.TextField(blank=True, help_text="Pronunciation tips")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:60]


class Paragraph(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True)
    topic = models.CharField(max_length=100, blank=True)
    word_count = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    comprehension_questions = models.TextField(blank=True,
                                               help_text="Add questions line by line")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.word_count = len(self.content.split())
        super().save(*args, **kwargs)


class Vocabulary(models.Model):
    word = models.CharField(max_length=200)
    definition = models.TextField()
    part_of_speech = models.CharField(max_length=50, blank=True)
    example = models.TextField(blank=True)
    synonyms = models.CharField(max_length=300, blank=True)
    antonyms = models.CharField(max_length=300, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name_plural = "Vocabularies"


# ─── WRITING ───────────────────────────────────────────────────────────────────

class WritingPrompt(models.Model):
    title = models.CharField(max_length=200)
    prompt_text = models.TextField()
    instructions = models.TextField(blank=True)
    word_limit = models.PositiveIntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WritingExercise(models.Model):
    EXERCISE_TYPES = [
        ('essay', 'Essay'),
        ('letter', 'Letter'),
        ('story', 'Story'),
        ('email', 'Email'),
        ('report', 'Report'),
    ]
    title = models.CharField(max_length=200)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES, default='essay')
    description = models.TextField()
    sample_answer = models.TextField(blank=True)
    tips = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GrammarRule(models.Model):
    title = models.CharField(max_length=200)
    rule = models.TextField()
    examples = models.TextField(blank=True)
    common_mistakes = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ─── LISTENING ─────────────────────────────────────────────────────────────────

class ListeningTrack(models.Model):
    TRACK_TYPES = [
        ('dialogue', 'Dialogue'),
        ('monologue', 'Monologue'),
        ('interview', 'Interview'),
        ('news', 'News Report'),
        ('podcast', 'Podcast'),
    ]
    title = models.CharField(max_length=200)
    track_type = models.CharField(max_length=20, choices=TRACK_TYPES, default='dialogue')
    description = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)
    transcript = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def duration_display(self):
        if self.duration_seconds:
            m, s = divmod(self.duration_seconds, 60)
            return f"{m}:{s:02d}"
        return "—"


class ListeningExercise(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    questions = models.TextField(help_text="Add questions line by line")
    answer_key = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Dictation(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    audio_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ─── SPEAKING ──────────────────────────────────────────────────────────────────

class SpeakingTopic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discussion_questions = models.TextField(blank=True)
    useful_phrases = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Pronunciation(models.Model):
    word_or_phrase = models.CharField(max_length=200)
    phonetic = models.CharField(max_length=200, blank=True, help_text="IPA transcription")
    tips = models.TextField()
    common_errors = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word_or_phrase


class Roleplay(models.Model):
    title = models.CharField(max_length=200)
    scenario = models.TextField()
    roles = models.TextField(help_text="Describe each role on a new line")
    objectives = models.TextField(blank=True)
    sample_dialogue = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
