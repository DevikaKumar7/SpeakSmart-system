from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (
    Schedule, Phrase, Paragraph, Vocabulary,
    WritingPrompt, WritingExercise, GrammarRule,
    ListeningTrack, ListeningExercise, Dictation,
    SpeakingTopic, Pronunciation, Roleplay
)
from .forms import (
    ScheduleForm, PhraseForm, ParagraphForm, VocabularyForm,
    WritingPromptForm, WritingExerciseForm, GrammarRuleForm,
    ListeningTrackForm, ListeningExerciseForm, DictationForm,
    SpeakingTopicForm, PronunciationForm, RoleplayForm
)


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@login_required
def scheduling_dashboard(request):
    context = {
        'phrase_count': Phrase.objects.filter(is_active=True).count(),
        'paragraph_count': Paragraph.objects.filter(is_active=True).count(),
        'vocabulary_count': Vocabulary.objects.filter(is_active=True).count(),
        'writing_prompt_count': WritingPrompt.objects.filter(is_active=True).count(),
        'writing_exercise_count': WritingExercise.objects.filter(is_active=True).count(),
        'grammar_rule_count': GrammarRule.objects.filter(is_active=True).count(),
        'track_count': ListeningTrack.objects.filter(is_active=True).count(),
        'listening_exercise_count': ListeningExercise.objects.filter(is_active=True).count(),
        'dictation_count': Dictation.objects.filter(is_active=True).count(),
        'speaking_topic_count': SpeakingTopic.objects.filter(is_active=True).count(),
        'pronunciation_count': Pronunciation.objects.filter(is_active=True).count(),
        'roleplay_count': Roleplay.objects.filter(is_active=True).count(),
    }
    return render(request, 'scheduling/dashboard.html', context)


# ─── GENERIC HELPERS ──────────────────────────────────────────────────────────

def _list_view(request, model, template, extra_ctx=None):
    search = request.GET.get('search', '')
    diff = request.GET.get('difficulty', '')
    show_all = request.GET.get('show_all', '')
    qs = model.objects.all()
    if not show_all:
        qs = qs.filter(is_active=True)
    if diff:
        qs = qs.filter(difficulty=diff)
    if search and hasattr(model, 'text'):
        qs = qs.filter(Q(text__icontains=search))
    elif search and hasattr(model, 'title'):
        qs = qs.filter(Q(title__icontains=search))
    ctx = {'items': qs.order_by('-created_at'), 'search': search,
           'difficulty': diff, 'show_all': show_all}
    if extra_ctx:
        ctx.update(extra_ctx)
    return render(request, template, ctx)


def _toggle(request, model, pk, redirect_url):
    obj = get_object_or_404(model, pk=pk)
    obj.is_active = not obj.is_active
    obj.save()
    status = 'enabled' if obj.is_active else 'disabled'
    messages.success(request, f'Item {status} successfully.')
    return redirect(redirect_url)


def _delete(request, model, pk, redirect_url):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        name = str(obj)
        obj.delete()
        messages.success(request, f'"{name}" deleted successfully.')
        return redirect(redirect_url)
    return render(request, 'scheduling/confirm_delete.html', {'obj': obj})


def _create(request, form_class, redirect_url, template, extra_ctx=None):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, 'Created successfully!')
            return redirect(redirect_url)
    else:
        form = form_class()
    ctx = {'form': form}
    if extra_ctx:
        ctx.update(extra_ctx)
    return render(request, template, ctx)


def _edit(request, model, pk, form_class, redirect_url, template, extra_ctx=None):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully!')
            return redirect(redirect_url)
    else:
        form = form_class(instance=obj)
    ctx = {'form': form, 'obj': obj}
    if extra_ctx:
        ctx.update(extra_ctx)
    return render(request, template, ctx)


# ─── READING: PHRASES ─────────────────────────────────────────────────────────

@login_required
def phrase_list(request):
    return _list_view(request, Phrase, 'scheduling/reading/phrase_list.html')

@login_required
def phrase_detail(request, pk):
    phrase = get_object_or_404(Phrase, pk=pk)
    return render(request, 'scheduling/reading/phrase_detail.html', {'obj': phrase})

@login_required
def phrase_create(request):
    return _create(request, PhraseForm, 'scheduling:phrase_list',
                   'scheduling/reading/phrase_form.html', {'title': 'Add Phrase', 'back_url': 'scheduling:phrase_list'})

@login_required
def phrase_edit(request, pk):
    return _edit(request, Phrase, pk, PhraseForm, 'scheduling:phrase_list',
                 'scheduling/reading/phrase_form.html', {'title': 'Edit Phrase', 'back_url': 'scheduling:phrase_list'})

@login_required
def phrase_delete(request, pk):
    return _delete(request, Phrase, pk, 'scheduling:phrase_list')

@login_required
def phrase_toggle(request, pk):
    return _toggle(request, Phrase, pk, 'scheduling:phrase_list')


# ─── READING: PARAGRAPHS ──────────────────────────────────────────────────────

@login_required
def paragraph_list(request):
    return _list_view(request, Paragraph, 'scheduling/reading/paragraph_list.html')

@login_required
def paragraph_detail(request, pk):
    obj = get_object_or_404(Paragraph, pk=pk)
    questions = [q.strip() for q in obj.comprehension_questions.split('\n') if q.strip()]
    return render(request, 'scheduling/reading/paragraph_detail.html', {'obj': obj, 'questions': questions})

@login_required
def paragraph_create(request):
    return _create(request, ParagraphForm, 'scheduling:paragraph_list',
                   'scheduling/reading/paragraph_form.html', {'title': 'Add Paragraph'})

@login_required
def paragraph_edit(request, pk):
    return _edit(request, Paragraph, pk, ParagraphForm, 'scheduling:paragraph_list',
                 'scheduling/reading/paragraph_form.html', {'title': 'Edit Paragraph'})

@login_required
def paragraph_delete(request, pk):
    return _delete(request, Paragraph, pk, 'scheduling:paragraph_list')

@login_required
def paragraph_toggle(request, pk):
    return _toggle(request, Paragraph, pk, 'scheduling:paragraph_list')


# ─── READING: VOCABULARY ──────────────────────────────────────────────────────

@login_required
def vocabulary_list(request):
    return _list_view(request, Vocabulary, 'scheduling/reading/vocabulary_list.html')

@login_required
def vocabulary_detail(request, pk):
    return render(request, 'scheduling/reading/vocabulary_detail.html',
                  {'obj': get_object_or_404(Vocabulary, pk=pk)})

@login_required
def vocabulary_create(request):
    return _create(request, VocabularyForm, 'scheduling:vocabulary_list',
                   'scheduling/reading/vocabulary_form.html', {'title': 'Add Vocabulary'})

@login_required
def vocabulary_edit(request, pk):
    return _edit(request, Vocabulary, pk, VocabularyForm, 'scheduling:vocabulary_list',
                 'scheduling/reading/vocabulary_form.html', {'title': 'Edit Vocabulary'})

@login_required
def vocabulary_delete(request, pk):
    return _delete(request, Vocabulary, pk, 'scheduling:vocabulary_list')

@login_required
def vocabulary_toggle(request, pk):
    return _toggle(request, Vocabulary, pk, 'scheduling:vocabulary_list')


# ─── WRITING: PROMPTS ─────────────────────────────────────────────────────────

@login_required
def writing_prompt_list(request):
    return _list_view(request, WritingPrompt, 'scheduling/writing/prompt_list.html')

@login_required
def writing_prompt_detail(request, pk):
    return render(request, 'scheduling/writing/prompt_detail.html',
                  {'obj': get_object_or_404(WritingPrompt, pk=pk)})

@login_required
def writing_prompt_create(request):
    return _create(request, WritingPromptForm, 'scheduling:writing_prompt_list',
                   'scheduling/writing/prompt_form.html', {'title': 'Add Writing Prompt'})

@login_required
def writing_prompt_edit(request, pk):
    return _edit(request, WritingPrompt, pk, WritingPromptForm, 'scheduling:writing_prompt_list',
                 'scheduling/writing/prompt_form.html', {'title': 'Edit Writing Prompt'})

@login_required
def writing_prompt_delete(request, pk):
    return _delete(request, WritingPrompt, pk, 'scheduling:writing_prompt_list')

@login_required
def writing_prompt_toggle(request, pk):
    return _toggle(request, WritingPrompt, pk, 'scheduling:writing_prompt_list')


# ─── WRITING: EXERCISES ───────────────────────────────────────────────────────

@login_required
def writing_exercise_list(request):
    return _list_view(request, WritingExercise, 'scheduling/writing/exercise_list.html')

@login_required
def writing_exercise_detail(request, pk):
    return render(request, 'scheduling/writing/exercise_detail.html',
                  {'obj': get_object_or_404(WritingExercise, pk=pk)})

@login_required
def writing_exercise_create(request):
    return _create(request, WritingExerciseForm, 'scheduling:writing_exercise_list',
                   'scheduling/writing/exercise_form.html', {'title': 'Add Writing Exercise'})

@login_required
def writing_exercise_edit(request, pk):
    return _edit(request, WritingExercise, pk, WritingExerciseForm, 'scheduling:writing_exercise_list',
                 'scheduling/writing/exercise_form.html', {'title': 'Edit Writing Exercise'})

@login_required
def writing_exercise_delete(request, pk):
    return _delete(request, WritingExercise, pk, 'scheduling:writing_exercise_list')

@login_required
def writing_exercise_toggle(request, pk):
    return _toggle(request, WritingExercise, pk, 'scheduling:writing_exercise_list')


# ─── WRITING: GRAMMAR ─────────────────────────────────────────────────────────

@login_required
def grammar_rule_list(request):
    return _list_view(request, GrammarRule, 'scheduling/writing/grammar_list.html')

@login_required
def grammar_rule_detail(request, pk):
    return render(request, 'scheduling/writing/grammar_detail.html',
                  {'obj': get_object_or_404(GrammarRule, pk=pk)})

@login_required
def grammar_rule_create(request):
    return _create(request, GrammarRuleForm, 'scheduling:grammar_rule_list',
                   'scheduling/writing/grammar_form.html', {'title': 'Add Grammar Rule'})

@login_required
def grammar_rule_edit(request, pk):
    return _edit(request, GrammarRule, pk, GrammarRuleForm, 'scheduling:grammar_rule_list',
                 'scheduling/writing/grammar_form.html', {'title': 'Edit Grammar Rule'})

@login_required
def grammar_rule_delete(request, pk):
    return _delete(request, GrammarRule, pk, 'scheduling:grammar_rule_list')

@login_required
def grammar_rule_toggle(request, pk):
    return _toggle(request, GrammarRule, pk, 'scheduling:grammar_rule_list')


# ─── LISTENING: TRACKS ────────────────────────────────────────────────────────

@login_required
def listening_track_list(request):
    return _list_view(request, ListeningTrack, 'scheduling/listening/track_list.html')

@login_required
def listening_track_detail(request, pk):
    return render(request, 'scheduling/listening/track_detail.html',
                  {'obj': get_object_or_404(ListeningTrack, pk=pk)})

@login_required
def listening_track_create(request):
    return _create(request, ListeningTrackForm, 'scheduling:listening_track_list',
                   'scheduling/listening/track_form.html', {'title': 'Add Listening Track'})

@login_required
def listening_track_edit(request, pk):
    return _edit(request, ListeningTrack, pk, ListeningTrackForm, 'scheduling:listening_track_list',
                 'scheduling/listening/track_form.html', {'title': 'Edit Listening Track'})

@login_required
def listening_track_delete(request, pk):
    return _delete(request, ListeningTrack, pk, 'scheduling:listening_track_list')

@login_required
def listening_track_toggle(request, pk):
    return _toggle(request, ListeningTrack, pk, 'scheduling:listening_track_list')


# ─── LISTENING: EXERCISES ─────────────────────────────────────────────────────

@login_required
def listening_exercise_list(request):
    return _list_view(request, ListeningExercise, 'scheduling/listening/exercise_list.html')

@login_required
def listening_exercise_detail(request, pk):
    obj = get_object_or_404(ListeningExercise, pk=pk)
    questions = [q.strip() for q in obj.questions.split('\n') if q.strip()]
    return render(request, 'scheduling/listening/exercise_detail.html', {'obj': obj, 'questions': questions})

@login_required
def listening_exercise_create(request):
    return _create(request, ListeningExerciseForm, 'scheduling:listening_exercise_list',
                   'scheduling/listening/exercise_form.html', {'title': 'Add Listening Exercise'})

@login_required
def listening_exercise_edit(request, pk):
    return _edit(request, ListeningExercise, pk, ListeningExerciseForm, 'scheduling:listening_exercise_list',
                 'scheduling/listening/exercise_form.html', {'title': 'Edit Listening Exercise'})

@login_required
def listening_exercise_delete(request, pk):
    return _delete(request, ListeningExercise, pk, 'scheduling:listening_exercise_list')

@login_required
def listening_exercise_toggle(request, pk):
    return _toggle(request, ListeningExercise, pk, 'scheduling:listening_exercise_list')


# ─── LISTENING: DICTATION ─────────────────────────────────────────────────────

@login_required
def dictation_list(request):
    return _list_view(request, Dictation, 'scheduling/listening/dictation_list.html')

@login_required
def dictation_detail(request, pk):
    return render(request, 'scheduling/listening/dictation_detail.html',
                  {'obj': get_object_or_404(Dictation, pk=pk)})

@login_required
def dictation_create(request):
    return _create(request, DictationForm, 'scheduling:dictation_list',
                   'scheduling/listening/dictation_form.html', {'title': 'Add Dictation'})

@login_required
def dictation_edit(request, pk):
    return _edit(request, Dictation, pk, DictationForm, 'scheduling:dictation_list',
                 'scheduling/listening/dictation_form.html', {'title': 'Edit Dictation'})

@login_required
def dictation_delete(request, pk):
    return _delete(request, Dictation, pk, 'scheduling:dictation_list')

@login_required
def dictation_toggle(request, pk):
    return _toggle(request, Dictation, pk, 'scheduling:dictation_list')


# ─── SPEAKING: TOPICS ─────────────────────────────────────────────────────────

@login_required
def speaking_topic_list(request):
    return _list_view(request, SpeakingTopic, 'scheduling/speaking/topic_list.html')

@login_required
def speaking_topic_detail(request, pk):
    obj = get_object_or_404(SpeakingTopic, pk=pk)
    questions = [q.strip() for q in obj.discussion_questions.split('\n') if q.strip()]
    return render(request, 'scheduling/speaking/topic_detail.html', {'obj': obj, 'questions': questions})

@login_required
def speaking_topic_create(request):
    return _create(request, SpeakingTopicForm, 'scheduling:speaking_topic_list',
                   'scheduling/speaking/topic_form.html', {'title': 'Add Speaking Topic'})

@login_required
def speaking_topic_edit(request, pk):
    return _edit(request, SpeakingTopic, pk, SpeakingTopicForm, 'scheduling:speaking_topic_list',
                 'scheduling/speaking/topic_form.html', {'title': 'Edit Speaking Topic'})

@login_required
def speaking_topic_delete(request, pk):
    return _delete(request, SpeakingTopic, pk, 'scheduling:speaking_topic_list')

@login_required
def speaking_topic_toggle(request, pk):
    return _toggle(request, SpeakingTopic, pk, 'scheduling:speaking_topic_list')


# ─── SPEAKING: PRONUNCIATION ──────────────────────────────────────────────────

@login_required
def pronunciation_list(request):
    return _list_view(request, Pronunciation, 'scheduling/speaking/pronunciation_list.html')

@login_required
def pronunciation_detail(request, pk):
    return render(request, 'scheduling/speaking/pronunciation_detail.html',
                  {'obj': get_object_or_404(Pronunciation, pk=pk)})

@login_required
def pronunciation_create(request):
    return _create(request, PronunciationForm, 'scheduling:pronunciation_list',
                   'scheduling/speaking/pronunciation_form.html', {'title': 'Add Pronunciation'})

@login_required
def pronunciation_edit(request, pk):
    return _edit(request, Pronunciation, pk, PronunciationForm, 'scheduling:pronunciation_list',
                 'scheduling/speaking/pronunciation_form.html', {'title': 'Edit Pronunciation'})

@login_required
def pronunciation_delete(request, pk):
    return _delete(request, Pronunciation, pk, 'scheduling:pronunciation_list')

@login_required
def pronunciation_toggle(request, pk):
    return _toggle(request, Pronunciation, pk, 'scheduling:pronunciation_list')


# ─── SPEAKING: ROLEPLAY ───────────────────────────────────────────────────────

@login_required
def roleplay_list(request):
    return _list_view(request, Roleplay, 'scheduling/speaking/roleplay_list.html')

@login_required
def roleplay_detail(request, pk):
    obj = get_object_or_404(Roleplay, pk=pk)
    roles = [r.strip() for r in obj.roles.split('\n') if r.strip()]
    return render(request, 'scheduling/speaking/roleplay_detail.html', {'obj': obj, 'roles': roles})

@login_required
def roleplay_create(request):
    return _create(request, RoleplayForm, 'scheduling:roleplay_list',
                   'scheduling/speaking/roleplay_form.html', {'title': 'Add Roleplay'})

@login_required
def roleplay_edit(request, pk):
    return _edit(request, Roleplay, pk, RoleplayForm, 'scheduling:roleplay_list',
                 'scheduling/speaking/roleplay_form.html', {'title': 'Edit Roleplay'})

@login_required
def roleplay_delete(request, pk):
    return _delete(request, Roleplay, pk, 'scheduling:roleplay_list')

@login_required
def roleplay_toggle(request, pk):
    return _toggle(request, Roleplay, pk, 'scheduling:roleplay_list')
