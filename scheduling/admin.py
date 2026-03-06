from django.contrib import admin
from .models import (Phrase, Paragraph, Vocabulary, WritingPrompt, WritingExercise,
                     GrammarRule, ListeningTrack, ListeningExercise, Dictation,
                     SpeakingTopic, Pronunciation, Roleplay)

for model in [Phrase, Paragraph, Vocabulary, WritingPrompt, WritingExercise,
              GrammarRule, ListeningTrack, ListeningExercise, Dictation,
              SpeakingTopic, Pronunciation, Roleplay]:
    admin.site.register(model)
