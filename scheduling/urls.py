from django.urls import path
from . import views

app_name = 'scheduling'

urlpatterns = [
    path('', views.scheduling_dashboard, name='dashboard'),

    # ── Reading: Phrases ──────────────────────────────────────────────────────
    path('reading/phrases/', views.phrase_list, name='phrase_list'),
    path('reading/phrases/create/', views.phrase_create, name='phrase_create'),
    path('reading/phrases/<int:pk>/', views.phrase_detail, name='phrase_detail'),
    path('reading/phrases/<int:pk>/edit/', views.phrase_edit, name='phrase_edit'),
    path('reading/phrases/<int:pk>/delete/', views.phrase_delete, name='phrase_delete'),
    path('reading/phrases/<int:pk>/toggle/', views.phrase_toggle, name='phrase_toggle'),

    # ── Reading: Paragraphs ───────────────────────────────────────────────────
    path('reading/paragraphs/', views.paragraph_list, name='paragraph_list'),
    path('reading/paragraphs/create/', views.paragraph_create, name='paragraph_create'),
    path('reading/paragraphs/<int:pk>/', views.paragraph_detail, name='paragraph_detail'),
    path('reading/paragraphs/<int:pk>/edit/', views.paragraph_edit, name='paragraph_edit'),
    path('reading/paragraphs/<int:pk>/delete/', views.paragraph_delete, name='paragraph_delete'),
    path('reading/paragraphs/<int:pk>/toggle/', views.paragraph_toggle, name='paragraph_toggle'),

    # ── Reading: Vocabulary ───────────────────────────────────────────────────
    path('reading/vocabulary/', views.vocabulary_list, name='vocabulary_list'),
    path('reading/vocabulary/create/', views.vocabulary_create, name='vocabulary_create'),
    path('reading/vocabulary/<int:pk>/', views.vocabulary_detail, name='vocabulary_detail'),
    path('reading/vocabulary/<int:pk>/edit/', views.vocabulary_edit, name='vocabulary_edit'),
    path('reading/vocabulary/<int:pk>/delete/', views.vocabulary_delete, name='vocabulary_delete'),
    path('reading/vocabulary/<int:pk>/toggle/', views.vocabulary_toggle, name='vocabulary_toggle'),

    # ── Writing: Prompts ──────────────────────────────────────────────────────
    path('writing/prompts/', views.writing_prompt_list, name='writing_prompt_list'),
    path('writing/prompts/create/', views.writing_prompt_create, name='writing_prompt_create'),
    path('writing/prompts/<int:pk>/', views.writing_prompt_detail, name='writing_prompt_detail'),
    path('writing/prompts/<int:pk>/edit/', views.writing_prompt_edit, name='writing_prompt_edit'),
    path('writing/prompts/<int:pk>/delete/', views.writing_prompt_delete, name='writing_prompt_delete'),
    path('writing/prompts/<int:pk>/toggle/', views.writing_prompt_toggle, name='writing_prompt_toggle'),

    # ── Writing: Exercises ────────────────────────────────────────────────────
    path('writing/exercises/', views.writing_exercise_list, name='writing_exercise_list'),
    path('writing/exercises/create/', views.writing_exercise_create, name='writing_exercise_create'),
    path('writing/exercises/<int:pk>/', views.writing_exercise_detail, name='writing_exercise_detail'),
    path('writing/exercises/<int:pk>/edit/', views.writing_exercise_edit, name='writing_exercise_edit'),
    path('writing/exercises/<int:pk>/delete/', views.writing_exercise_delete, name='writing_exercise_delete'),
    path('writing/exercises/<int:pk>/toggle/', views.writing_exercise_toggle, name='writing_exercise_toggle'),

    # ── Writing: Grammar ──────────────────────────────────────────────────────
    path('writing/grammar/', views.grammar_rule_list, name='grammar_rule_list'),
    path('writing/grammar/create/', views.grammar_rule_create, name='grammar_rule_create'),
    path('writing/grammar/<int:pk>/', views.grammar_rule_detail, name='grammar_rule_detail'),
    path('writing/grammar/<int:pk>/edit/', views.grammar_rule_edit, name='grammar_rule_edit'),
    path('writing/grammar/<int:pk>/delete/', views.grammar_rule_delete, name='grammar_rule_delete'),
    path('writing/grammar/<int:pk>/toggle/', views.grammar_rule_toggle, name='grammar_rule_toggle'),

    # ── Listening: Tracks ─────────────────────────────────────────────────────
    path('listening/tracks/', views.listening_track_list, name='listening_track_list'),
    path('listening/tracks/create/', views.listening_track_create, name='listening_track_create'),
    path('listening/tracks/<int:pk>/', views.listening_track_detail, name='listening_track_detail'),
    path('listening/tracks/<int:pk>/edit/', views.listening_track_edit, name='listening_track_edit'),
    path('listening/tracks/<int:pk>/delete/', views.listening_track_delete, name='listening_track_delete'),
    path('listening/tracks/<int:pk>/toggle/', views.listening_track_toggle, name='listening_track_toggle'),

    # ── Listening: Exercises ──────────────────────────────────────────────────
    path('listening/exercises/', views.listening_exercise_list, name='listening_exercise_list'),
    path('listening/exercises/create/', views.listening_exercise_create, name='listening_exercise_create'),
    path('listening/exercises/<int:pk>/', views.listening_exercise_detail, name='listening_exercise_detail'),
    path('listening/exercises/<int:pk>/edit/', views.listening_exercise_edit, name='listening_exercise_edit'),
    path('listening/exercises/<int:pk>/delete/', views.listening_exercise_delete, name='listening_exercise_delete'),
    path('listening/exercises/<int:pk>/toggle/', views.listening_exercise_toggle, name='listening_exercise_toggle'),

    # ── Listening: Dictation ──────────────────────────────────────────────────
    path('listening/dictation/', views.dictation_list, name='dictation_list'),
    path('listening/dictation/create/', views.dictation_create, name='dictation_create'),
    path('listening/dictation/<int:pk>/', views.dictation_detail, name='dictation_detail'),
    path('listening/dictation/<int:pk>/edit/', views.dictation_edit, name='dictation_edit'),
    path('listening/dictation/<int:pk>/delete/', views.dictation_delete, name='dictation_delete'),
    path('listening/dictation/<int:pk>/toggle/', views.dictation_toggle, name='dictation_toggle'),

    # ── Speaking: Topics ──────────────────────────────────────────────────────
    path('speaking/topics/', views.speaking_topic_list, name='speaking_topic_list'),
    path('speaking/topics/create/', views.speaking_topic_create, name='speaking_topic_create'),
    path('speaking/topics/<int:pk>/', views.speaking_topic_detail, name='speaking_topic_detail'),
    path('speaking/topics/<int:pk>/edit/', views.speaking_topic_edit, name='speaking_topic_edit'),
    path('speaking/topics/<int:pk>/delete/', views.speaking_topic_delete, name='speaking_topic_delete'),
    path('speaking/topics/<int:pk>/toggle/', views.speaking_topic_toggle, name='speaking_topic_toggle'),

    # ── Speaking: Pronunciation ───────────────────────────────────────────────
    path('speaking/pronunciation/', views.pronunciation_list, name='pronunciation_list'),
    path('speaking/pronunciation/create/', views.pronunciation_create, name='pronunciation_create'),
    path('speaking/pronunciation/<int:pk>/', views.pronunciation_detail, name='pronunciation_detail'),
    path('speaking/pronunciation/<int:pk>/edit/', views.pronunciation_edit, name='pronunciation_edit'),
    path('speaking/pronunciation/<int:pk>/delete/', views.pronunciation_delete, name='pronunciation_delete'),
    path('speaking/pronunciation/<int:pk>/toggle/', views.pronunciation_toggle, name='speaking_pronunciation_toggle'),

    # ── Speaking: Roleplay ────────────────────────────────────────────────────
    path('speaking/roleplay/', views.roleplay_list, name='roleplay_list'),
    path('speaking/roleplay/create/', views.roleplay_create, name='roleplay_create'),
    path('speaking/roleplay/<int:pk>/', views.roleplay_detail, name='roleplay_detail'),
    path('speaking/roleplay/<int:pk>/edit/', views.roleplay_edit, name='roleplay_edit'),
    path('speaking/roleplay/<int:pk>/delete/', views.roleplay_delete, name='roleplay_delete'),
    path('speaking/roleplay/<int:pk>/toggle/', views.roleplay_toggle, name='roleplay_toggle'),
]
