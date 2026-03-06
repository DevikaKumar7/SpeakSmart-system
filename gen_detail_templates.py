import os

BASE = "/home/claude/english_course/scheduling/templates/scheduling"

def detail(path, title, icon, edit_url, delete_url, toggle_url, list_url, fields):
    fields_html = ""
    for label, field, is_long in fields:
        if is_long:
            fields_html += f"""<div class="detail-field" style="grid-column:1/-1"><label>{label}</label><div class="long-text">{{{{{field}}}}}</div></div>\n"""
        else:
            fields_html += f"""<div class="detail-field"><label>{label}</label><p>{{{{{field}}}}}</p></div>\n"""
    return f"""
{{% extends "base.html" %}}
{{% block title %}}{{{{ obj }}}}{{% endblock %}}
{{% block page_title %}}{icon} {title} Detail{{% endblock %}}
{{% block topbar_actions %}}
<a href="{{% url '{edit_url}' obj.pk %}}" class="btn btn-warning btn-sm">✏️ Edit</a>
<a href="{{% url '{toggle_url}' obj.pk %}}" class="btn btn-{{%if obj.is_active%}}warning{{%else%}}success{{%endif%}} btn-sm" onclick="return confirm('Toggle status?')">{{%if obj.is_active%}}🚫 Disable{{%else%}}✅ Enable{{%endif%}}</a>
<a href="{{% url '{delete_url}' obj.pk %}}" class="btn btn-danger btn-sm" onclick="return confirm('Delete permanently?')">🗑 Delete</a>
{{% endblock %}}
{{% block content %}}
<div class="card">
  <div class="card-header">
    <h3>{{{{ obj }}}}</h3>
    <div style="display:flex;gap:8px;align-items:center">
      <span class="badge badge-secondary">{{{{ obj.difficulty }}}}</span>
      <span class="badge badge-{{%if obj.is_active%}}success{{%else%}}danger{{%endif%}}">{{%if obj.is_active%}}Active{{%else%}}Disabled{{%endif%}}</span>
    </div>
  </div>
  <div class="card-body">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      {fields_html}
      <div class="detail-field"><label>Created By</label><p>{{{{ obj.created_by.get_full_name|default:obj.created_by.username|default:"—" }}}}</p></div>
      <div class="detail-field"><label>Created At</label><p>{{{{ obj.created_at|date:"M d, Y H:i" }}}}</p></div>
    </div>
  </div>
</div>
<a href="{{% url '{list_url}' %}}" class="btn btn-secondary">← Back to List</a>
{{% endblock %}}
""".strip()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f: f.write(content)
    print(f"  ✓ {path.split('scheduling/templates/scheduling/')[-1]}")

# Reading
write(f"{BASE}/reading/phrase_detail.html", detail(
    "reading","Phrase","💬","scheduling:phrase_edit","scheduling:phrase_delete",
    "scheduling:phrase_toggle","scheduling:phrase_list",
    [("Phrase Text","obj.text",False),("Meaning","obj.meaning",True),
     ("Example Sentence","obj.example_sentence",True),("Translation","obj.translation",False),
     ("Category","obj.category|default:'—'",False),("Pronunciation Tips","obj.audio_note",True)]))

write(f"{BASE}/reading/paragraph_detail.html",
f"""{{% extends "base.html" %}}
{{% block title %}}{{{{ obj.title }}}}{{% endblock %}}
{{% block page_title %}}📄 {{{{ obj.title }}}}{{% endblock %}}
{{% block topbar_actions %}}
<a href="{{% url 'scheduling:paragraph_edit' obj.pk %}}" class="btn btn-warning btn-sm">✏️ Edit</a>
<a href="{{% url 'scheduling:paragraph_toggle' obj.pk %}}" class="btn btn-{{%if obj.is_active%}}warning{{%else%}}success{{%endif%}} btn-sm" onclick="return confirm('Toggle?')">{{%if obj.is_active%}}🚫 Disable{{%else%}}✅ Enable{{%endif%}}</a>
<a href="{{% url 'scheduling:paragraph_delete' obj.pk %}}" class="btn btn-danger btn-sm" onclick="return confirm('Delete?')">🗑</a>
{{% endblock %}}
{{% block content %}}
<div class="card">
  <div class="card-header"><h3>{{{{ obj.title }}}}<span style="margin-left:10px" class="badge badge-secondary">{{{{ obj.difficulty }}}}</span><span style="margin-left:6px" class="badge badge-{{%if obj.is_active%}}success{{%else%}}danger{{%endif%}}">{{%if obj.is_active%}}Active{{%else%}}Disabled{{%endif%}}</span></h3></div>
  <div class="card-body">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
      <div class="detail-field"><label>Topic</label><p>{{{{ obj.topic|default:"—" }}}}</p></div>
      <div class="detail-field"><label>Word Count</label><p>{{{{ obj.word_count }}}}</p></div>
    </div>
    <div class="detail-field"><label>Content</label><div class="long-text">{{{{ obj.content }}}}</div></div>
    {{%if obj.summary%}}<div class="detail-field" style="margin-top:16px"><label>Summary</label><div class="long-text">{{{{ obj.summary }}}}</div></div>{{%endif%}}
    {{%if questions%}}<div class="detail-field" style="margin-top:16px"><label>Comprehension Questions</label><ol style="margin-left:20px;line-height:2">{{%for q in questions%}}<li>{{{{ q }}}}</li>{{%endfor%}}</ol></div>{{%endif%}}
  </div>
</div>
<a href="{{% url 'scheduling:paragraph_list' %}}" class="btn btn-secondary">← Back</a>
{{% endblock %}}""")

write(f"{BASE}/reading/vocabulary_detail.html", detail(
    "reading","Vocabulary","🔤","scheduling:vocabulary_edit","scheduling:vocabulary_delete",
    "scheduling:vocabulary_toggle","scheduling:vocabulary_list",
    [("Word","obj.word",False),("Part of Speech","obj.part_of_speech|default:'—'",False),
     ("Definition","obj.definition",True),("Example","obj.example",True),
     ("Synonyms","obj.synonyms|default:'—'",False),("Antonyms","obj.antonyms|default:'—'",False)]))

# Writing
write(f"{BASE}/writing/prompt_detail.html", detail(
    "writing","Writing Prompt","💡","scheduling:writing_prompt_edit","scheduling:writing_prompt_delete",
    "scheduling:writing_prompt_toggle","scheduling:writing_prompt_list",
    [("Title","obj.title",False),("Word Limit","obj.word_limit|default:'No limit'",False),
     ("Prompt","obj.prompt_text",True),("Instructions","obj.instructions",True)]))

write(f"{BASE}/writing/exercise_detail.html", detail(
    "writing","Writing Exercise","📝","scheduling:writing_exercise_edit","scheduling:writing_exercise_delete",
    "scheduling:writing_exercise_toggle","scheduling:writing_exercise_list",
    [("Title","obj.title",False),("Type","obj.get_exercise_type_display",False),
     ("Description","obj.description",True),("Tips","obj.tips",True),
     ("Sample Answer","obj.sample_answer",True)]))

write(f"{BASE}/writing/grammar_detail.html", detail(
    "writing","Grammar Rule","📐","scheduling:grammar_rule_edit","scheduling:grammar_rule_delete",
    "scheduling:grammar_rule_toggle","scheduling:grammar_rule_list",
    [("Title","obj.title",False),("Rule","obj.rule",True),
     ("Examples","obj.examples",True),("Common Mistakes","obj.common_mistakes",True)]))

# Listening
write(f"{BASE}/listening/track_detail.html", detail(
    "listening","Listening Track","🎵","scheduling:listening_track_edit","scheduling:listening_track_delete",
    "scheduling:listening_track_toggle","scheduling:listening_track_list",
    [("Title","obj.title",False),("Type","obj.get_track_type_display",False),
     ("Duration","obj.duration_display",False),("Audio URL","obj.audio_url|default:'—'",False),
     ("Description","obj.description",True),("Transcript","obj.transcript",True)]))

write(f"{BASE}/listening/exercise_detail.html",
f"""{{% extends "base.html" %}}
{{% block title %}}{{{{ obj.title }}}}{{% endblock %}}
{{% block page_title %}}❓ {{{{ obj.title }}}}{{% endblock %}}
{{% block topbar_actions %}}<a href="{{% url 'scheduling:listening_exercise_edit' obj.pk %}}" class="btn btn-warning btn-sm">✏️ Edit</a><a href="{{% url 'scheduling:listening_exercise_delete' obj.pk %}}" class="btn btn-danger btn-sm" onclick="return confirm('Delete?')">🗑</a>{{% endblock %}}
{{% block content %}}
<div class="card">
  <div class="card-header"><h3>{{{{ obj.title }}}}<span style="margin-left:10px" class="badge badge-secondary">{{{{ obj.difficulty }}}}</span></h3></div>
  <div class="card-body">
    <div class="detail-field"><label>Instructions</label><div class="long-text">{{{{ obj.instructions }}}}</div></div>
    {{%if questions%}}<div class="detail-field" style="margin-top:16px"><label>Questions</label><ol style="margin-left:20px;line-height:2">{{%for q in questions%}}<li>{{{{ q }}}}</li>{{%endfor%}}</ol></div>{{%endif%}}
    {{%if obj.answer_key%}}<div class="detail-field" style="margin-top:16px"><label>Answer Key</label><div class="long-text">{{{{ obj.answer_key }}}}</div></div>{{%endif%}}
  </div>
</div>
<a href="{{% url 'scheduling:listening_exercise_list' %}}" class="btn btn-secondary">← Back</a>
{{% endblock %}}""")

write(f"{BASE}/listening/dictation_detail.html", detail(
    "listening","Dictation","✏️","scheduling:dictation_edit","scheduling:dictation_delete",
    "scheduling:dictation_toggle","scheduling:dictation_list",
    [("Title","obj.title",False),("Audio URL","obj.audio_url|default:'—'",False),
     ("Text","obj.text",True),("Notes","obj.notes",True)]))

# Speaking
write(f"{BASE}/speaking/topic_detail.html",
f"""{{% extends "base.html" %}}
{{% block title %}}{{{{ obj.title }}}}{{% endblock %}}
{{% block page_title %}}💭 {{{{ obj.title }}}}{{% endblock %}}
{{% block topbar_actions %}}<a href="{{% url 'scheduling:speaking_topic_edit' obj.pk %}}" class="btn btn-warning btn-sm">✏️ Edit</a><a href="{{% url 'scheduling:speaking_topic_delete' obj.pk %}}" class="btn btn-danger btn-sm" onclick="return confirm('Delete?')">🗑</a>{{% endblock %}}
{{% block content %}}
<div class="card">
  <div class="card-header"><h3>{{{{ obj.title }}}}<span style="margin-left:10px" class="badge badge-secondary">{{{{ obj.difficulty }}}}</span>{{%if obj.time_limit_minutes%}}<span style="margin-left:6px" class="badge badge-primary">{{{{ obj.time_limit_minutes }}}} min</span>{{%endif%}}</h3></div>
  <div class="card-body">
    <div class="detail-field"><label>Description</label><div class="long-text">{{{{ obj.description }}}}</div></div>
    {{%if questions%}}<div class="detail-field" style="margin-top:16px"><label>Discussion Questions</label><ol style="margin-left:20px;line-height:2">{{%for q in questions%}}<li>{{{{ q }}}}</li>{{%endfor%}}</ol></div>{{%endif%}}
    {{%if obj.useful_phrases%}}<div class="detail-field" style="margin-top:16px"><label>Useful Phrases</label><div class="long-text">{{{{ obj.useful_phrases }}}}</div></div>{{%endif%}}
  </div>
</div>
<a href="{{% url 'scheduling:speaking_topic_list' %}}" class="btn btn-secondary">← Back</a>
{{% endblock %}}""")

write(f"{BASE}/speaking/pronunciation_detail.html", detail(
    "speaking","Pronunciation","🔊","scheduling:pronunciation_edit","scheduling:pronunciation_delete",
    "scheduling:speaking_pronunciation_toggle","scheduling:pronunciation_list",
    [("Word/Phrase","obj.word_or_phrase",False),("Phonetic (IPA)","obj.phonetic|default:'—'",False),
     ("Audio URL","obj.audio_url|default:'—'",False),("Tips","obj.tips",True),
     ("Common Errors","obj.common_errors",True)]))

write(f"{BASE}/speaking/roleplay_detail.html",
f"""{{% extends "base.html" %}}
{{% block title %}}{{{{ obj.title }}}}{{% endblock %}}
{{% block page_title %}}🎭 {{{{ obj.title }}}}{{% endblock %}}
{{% block topbar_actions %}}<a href="{{% url 'scheduling:roleplay_edit' obj.pk %}}" class="btn btn-warning btn-sm">✏️ Edit</a><a href="{{% url 'scheduling:roleplay_delete' obj.pk %}}" class="btn btn-danger btn-sm" onclick="return confirm('Delete?')">🗑</a>{{% endblock %}}
{{% block content %}}
<div class="card">
  <div class="card-header"><h3>{{{{ obj.title }}}}<span style="margin-left:10px" class="badge badge-secondary">{{{{ obj.difficulty }}}}</span></h3></div>
  <div class="card-body">
    <div class="detail-field"><label>Scenario</label><div class="long-text">{{{{ obj.scenario }}}}</div></div>
    {{%if roles%}}<div class="detail-field" style="margin-top:16px"><label>Roles</label><ul style="margin-left:20px;line-height:2">{{%for r in roles%}}<li>{{{{ r }}}}</li>{{%endfor%}}</ul></div>{{%endif%}}
    {{%if obj.objectives%}}<div class="detail-field" style="margin-top:16px"><label>Objectives</label><div class="long-text">{{{{ obj.objectives }}}}</div></div>{{%endif%}}
    {{%if obj.sample_dialogue%}}<div class="detail-field" style="margin-top:16px"><label>Sample Dialogue</label><div class="long-text">{{{{ obj.sample_dialogue }}}}</div></div>{{%endif%}}
  </div>
</div>
<a href="{{% url 'scheduling:roleplay_list' %}}" class="btn btn-secondary">← Back</a>
{{% endblock %}}""")

print("✅ All detail templates generated!")
