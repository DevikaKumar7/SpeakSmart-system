from django import forms
from .models import (
    Schedule, Phrase, Paragraph, Vocabulary,
    WritingPrompt, WritingExercise, GrammarRule,
    ListeningTrack, ListeningExercise, Dictation,
    SpeakingTopic, Pronunciation, Roleplay
)

TEXTAREA_WIDGET = forms.Textarea(attrs={'rows': 4})

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'batch', 'description', 'date']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'description': TEXTAREA_WIDGET}

class PhraseForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = ['text', 'meaning', 'example_sentence', 'translation', 'difficulty', 'category', 'audio_note']
        widgets = {'meaning': TEXTAREA_WIDGET, 'example_sentence': TEXTAREA_WIDGET, 'audio_note': TEXTAREA_WIDGET}

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['title', 'content', 'summary', 'topic', 'difficulty', 'comprehension_questions']
        widgets = {'content': forms.Textarea(attrs={'rows': 8}), 'summary': TEXTAREA_WIDGET,
                   'comprehension_questions': TEXTAREA_WIDGET}

class VocabularyForm(forms.ModelForm):
    class Meta:
        model = Vocabulary
        fields = ['word', 'definition', 'part_of_speech', 'example', 'synonyms', 'antonyms', 'difficulty']
        widgets = {'definition': TEXTAREA_WIDGET, 'example': TEXTAREA_WIDGET}

class WritingPromptForm(forms.ModelForm):
    class Meta:
        model = WritingPrompt
        fields = ['title', 'prompt_text', 'instructions', 'word_limit', 'difficulty']
        widgets = {'prompt_text': TEXTAREA_WIDGET, 'instructions': TEXTAREA_WIDGET}

class WritingExerciseForm(forms.ModelForm):
    class Meta:
        model = WritingExercise
        fields = ['title', 'exercise_type', 'description', 'sample_answer', 'tips', 'difficulty']
        widgets = {'description': TEXTAREA_WIDGET, 'sample_answer': forms.Textarea(attrs={'rows': 6}),
                   'tips': TEXTAREA_WIDGET}

class GrammarRuleForm(forms.ModelForm):
    class Meta:
        model = GrammarRule
        fields = ['title', 'rule', 'examples', 'common_mistakes', 'difficulty']
        widgets = {'rule': TEXTAREA_WIDGET, 'examples': TEXTAREA_WIDGET, 'common_mistakes': TEXTAREA_WIDGET}

class ListeningTrackForm(forms.ModelForm):
    class Meta:
        model = ListeningTrack
        fields = ['title', 'track_type', 'description', 'audio_url', 'transcript', 'duration_seconds', 'difficulty']
        widgets = {'description': TEXTAREA_WIDGET, 'transcript': forms.Textarea(attrs={'rows': 6})}

class ListeningExerciseForm(forms.ModelForm):
    class Meta:
        model = ListeningExercise
        fields = ['title', 'instructions', 'questions', 'answer_key', 'difficulty']
        widgets = {'instructions': TEXTAREA_WIDGET, 'questions': TEXTAREA_WIDGET, 'answer_key': TEXTAREA_WIDGET}

class DictationForm(forms.ModelForm):
    class Meta:
        model = Dictation
        fields = ['title', 'text', 'audio_url', 'notes', 'difficulty']
        widgets = {'text': forms.Textarea(attrs={'rows': 6}), 'notes': TEXTAREA_WIDGET}

class SpeakingTopicForm(forms.ModelForm):
    class Meta:
        model = SpeakingTopic
        fields = ['title', 'description', 'discussion_questions', 'useful_phrases', 'time_limit_minutes', 'difficulty']
        widgets = {'description': TEXTAREA_WIDGET, 'discussion_questions': TEXTAREA_WIDGET,
                   'useful_phrases': TEXTAREA_WIDGET}

class PronunciationForm(forms.ModelForm):
    class Meta:
        model = Pronunciation
        fields = ['word_or_phrase', 'phonetic', 'tips', 'common_errors', 'audio_url', 'difficulty']
        widgets = {'tips': TEXTAREA_WIDGET, 'common_errors': TEXTAREA_WIDGET}

class RoleplayForm(forms.ModelForm):
    class Meta:
        model = Roleplay
        fields = ['title', 'scenario', 'roles', 'objectives', 'sample_dialogue', 'difficulty']
        widgets = {'scenario': TEXTAREA_WIDGET, 'roles': TEXTAREA_WIDGET,
                   'objectives': TEXTAREA_WIDGET, 'sample_dialogue': forms.Textarea(attrs={'rows': 6})}
