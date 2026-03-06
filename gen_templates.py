import os

BASE = "/home/claude/english_course/scheduling/templates/scheduling"

def make_list(folder, name, title, icon, create_url, detail_url, edit_url, delete_url, toggle_url, fields_display, color="primary"):
    return f"""
{{% extends "base.html" %}}
{{% block title %}}{title}{{% endblock %}}
{{% block page_title %}}{icon} {title}{{% endblock %}}
{{% block topbar_actions %}}<a href="{{% url '{create_url}' %}}" class="btn btn-primary">+ Add {title[:-1] if title.endswith('s') else title}</a>{{% endblock %}}
{{% block content %}}
<div class="search-bar">
  <form method="get" style="display:flex;gap:10px;flex-wrap:wrap;width:100%">
    <input name="search" value="{{{{ search }}}}" placeholder="🔍 Search..." style="flex:1;min-width:200px">
    <select name="difficulty">
      <option value="">All Levels</option>
      <option value="beginner" {{%if difficulty == 'beginner'%}}selected{{%endif%}}>Beginner</option>
      <option value="intermediate" {{%if difficulty == 'intermediate'%}}selected{{%endif%}}>Intermediate</option>
      <option value="advanced" {{%if difficulty == 'advanced'%}}selected{{%endif%}}>Advanced</option>
    </select>
    <label style="display:flex;align-items:center;gap:6px;font-size:.85rem"><input type="checkbox" name="show_all" {{%if show_all%}}checked{{%endif%}} value="1"> Show Disabled</label>
    <button type="submit" class="btn btn-primary">Search</button>
    <a href="{{% url '{create_url}' %}}" class="btn btn-secondary">Clear</a>
  </form>
</div>
<div class="card">
  <div class="card-body" style="padding:0">
    <table>
      <thead><tr><th>{fields_display[0][0]}</th><th>Difficulty</th><th>Status</th><th>Created</th><th>Actions</th></tr></thead>
      <tbody>
      {{%for item in items%}}
      <tr>
        <td><a href="{{% url '{detail_url}' item.pk %}}" style="font-weight:600;color:#2563eb;text-decoration:none">{{{{ {fields_display[0][1]} }}}}</a></td>
        <td><span class="badge badge-secondary">{{{{ item.difficulty }}}}</span></td>
        <td><span class="badge badge-{{%if item.is_active%}}success{{%else%}}danger{{%endif%}}">{{%if item.is_active%}}Active{{%else%}}Disabled{{%endif%}}</span></td>
        <td style="color:#64748b;font-size:.8rem">{{{{ item.created_at|date:"M d, Y" }}}}</td>
        <td class="action-buttons">
          <a href="{{% url '{detail_url}' item.pk %}}" class="btn btn-secondary btn-sm">👁</a>
          <a href="{{% url '{edit_url}' item.pk %}}" class="btn btn-warning btn-sm">✏️</a>
          <a href="{{% url '{toggle_url}' item.pk %}}" class="btn btn-{{%if item.is_active%}}warning{{%else%}}success{{%endif%}} btn-sm" onclick="return confirm('Toggle status?')">{{%if item.is_active%}}🚫{{%else%}}✅{{%endif%}}</a>
          <a href="{{% url '{delete_url}' item.pk %}}" class="btn btn-danger btn-sm" onclick="return confirm('Delete permanently?')">🗑</a>
        </td>
      </tr>
      {{%empty%}}
      <tr><td colspan="5"><div class="empty-state"><div class="icon">{icon}</div><p>No {title.lower()} yet.<br><a href="{{% url '{create_url}' %}}">Add one now</a></p></div></td></tr>
      {{%endfor%}}
      </tbody>
    </table>
  </div>
</div>
{{% endblock %}}
""".strip()


def make_form(folder, name, title, back_url, fields_help=""):
    return f"""
{{% extends "base.html" %}}
{{% block title %}}{{{{ title }}}}{{% endblock %}}
{{% block page_title %}}{{{{ title }}}}{{% endblock %}}
{{% block content %}}
<div style="max-width:700px;margin:0 auto">
<div class="card">
  <div class="card-header"><h3>{{{{ title }}}}</h3></div>
  <div class="card-body">
    <form method="post">{{%csrf_token%}}
      {{%for field in form%}}
      <div class="form-group">
        <label>{{{{ field.label }}}}</label>
        {{{{ field }}}}
        {{%if field.help_text%}}<p class="help">{{{{ field.help_text }}}}</p>{{%endif%}}
        {{%if field.errors%}}<p style="color:red;font-size:.8rem">{{{{ field.errors.0 }}}}</p>{{%endif%}}
      </div>
      {{%endfor%}}
      <div style="display:flex;gap:10px;margin-top:8px">
        <button type="submit" class="btn btn-primary">✅ Save</button>
        <a href="{{% url '{back_url}' %}}" class="btn btn-secondary">Cancel</a>
      </div>
    </form>
  </div>
</div>
</div>
{{% endblock %}}
""".strip()


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✓ {path.split('scheduling/templates/scheduling/')[-1]}")


# ── READING ────────────────────────────────────────────────────────────────────
print("Reading templates...")

write(f"{BASE}/reading/phrase_list.html",
      make_list("reading","phrase","Phrases","💬","scheduling:phrase_create","scheduling:phrase_detail",
                "scheduling:phrase_edit","scheduling:phrase_delete","scheduling:phrase_toggle",
                [("Phrase Text","item.text|truncatechars:60")]))

write(f"{BASE}/reading/paragraph_list.html",
      make_list("reading","paragraph","Paragraphs","📄","scheduling:paragraph_create","scheduling:paragraph_detail",
                "scheduling:paragraph_edit","scheduling:paragraph_delete","scheduling:paragraph_toggle",
                [("Title","item.title")]))

write(f"{BASE}/reading/vocabulary_list.html",
      make_list("reading","vocabulary","Vocabulary","🔤","scheduling:vocabulary_create","scheduling:vocabulary_detail",
                "scheduling:vocabulary_edit","scheduling:vocabulary_delete","scheduling:vocabulary_toggle",
                [("Word","item.word")]))

write(f"{BASE}/reading/phrase_form.html", make_form("reading","phrase","Phrase","scheduling:phrase_list"))
write(f"{BASE}/reading/paragraph_form.html", make_form("reading","paragraph","Paragraph","scheduling:paragraph_list"))
write(f"{BASE}/reading/vocabulary_form.html", make_form("reading","vocabulary","Vocabulary","scheduling:vocabulary_list"))

# ── WRITING ────────────────────────────────────────────────────────────────────
print("Writing templates...")

write(f"{BASE}/writing/prompt_list.html",
      make_list("writing","prompt","Writing Prompts","💡","scheduling:writing_prompt_create","scheduling:writing_prompt_detail",
                "scheduling:writing_prompt_edit","scheduling:writing_prompt_delete","scheduling:writing_prompt_toggle",
                [("Title","item.title")]))

write(f"{BASE}/writing/exercise_list.html",
      make_list("writing","exercise","Writing Exercises","📝","scheduling:writing_exercise_create","scheduling:writing_exercise_detail",
                "scheduling:writing_exercise_edit","scheduling:writing_exercise_delete","scheduling:writing_exercise_toggle",
                [("Title","item.title")]))

write(f"{BASE}/writing/grammar_list.html",
      make_list("writing","grammar","Grammar Rules","📐","scheduling:grammar_rule_create","scheduling:grammar_rule_detail",
                "scheduling:grammar_rule_edit","scheduling:grammar_rule_delete","scheduling:grammar_rule_toggle",
                [("Title","item.title")]))

write(f"{BASE}/writing/prompt_form.html", make_form("writing","prompt","Writing Prompt","scheduling:writing_prompt_list"))
write(f"{BASE}/writing/exercise_form.html", make_form("writing","exercise","Writing Exercise","scheduling:writing_exercise_list"))
write(f"{BASE}/writing/grammar_form.html", make_form("writing","grammar","Grammar Rule","scheduling:grammar_rule_list"))

# ── LISTENING ──────────────────────────────────────────────────────────────────
print("Listening templates...")

write(f"{BASE}/listening/track_list.html",
      make_list("listening","track","Listening Tracks","🎵","scheduling:listening_track_create","scheduling:listening_track_detail",
                "scheduling:listening_track_edit","scheduling:listening_track_delete","scheduling:listening_track_toggle",
                [("Title","item.title")]))

write(f"{BASE}/listening/exercise_list.html",
      make_list("listening","exercise","Listening Exercises","❓","scheduling:listening_exercise_create","scheduling:listening_exercise_detail",
                "scheduling:listening_exercise_edit","scheduling:listening_exercise_delete","scheduling:listening_exercise_toggle",
                [("Title","item.title")]))

write(f"{BASE}/listening/dictation_list.html",
      make_list("listening","dictation","Dictation","✏️","scheduling:dictation_create","scheduling:dictation_detail",
                "scheduling:dictation_edit","scheduling:dictation_delete","scheduling:dictation_toggle",
                [("Title","item.title")]))

write(f"{BASE}/listening/track_form.html", make_form("listening","track","Listening Track","scheduling:listening_track_list"))
write(f"{BASE}/listening/exercise_form.html", make_form("listening","exercise","Listening Exercise","scheduling:listening_exercise_list"))
write(f"{BASE}/listening/dictation_form.html", make_form("listening","dictation","Dictation","scheduling:dictation_list"))

# ── SPEAKING ───────────────────────────────────────────────────────────────────
print("Speaking templates...")

write(f"{BASE}/speaking/topic_list.html",
      make_list("speaking","topic","Speaking Topics","💭","scheduling:speaking_topic_create","scheduling:speaking_topic_detail",
                "scheduling:speaking_topic_edit","scheduling:speaking_topic_delete","scheduling:speaking_topic_toggle",
                [("Title","item.title")]))

write(f"{BASE}/speaking/pronunciation_list.html",
      make_list("speaking","pronunciation","Pronunciation","🔊","scheduling:pronunciation_create","scheduling:pronunciation_detail",
                "scheduling:pronunciation_edit","scheduling:pronunciation_delete","scheduling:speaking_pronunciation_toggle",
                [("Word/Phrase","item.word_or_phrase")]))

write(f"{BASE}/speaking/roleplay_list.html",
      make_list("speaking","roleplay","Roleplay Scenarios","🎭","scheduling:roleplay_create","scheduling:roleplay_detail",
                "scheduling:roleplay_edit","scheduling:roleplay_delete","scheduling:roleplay_toggle",
                [("Title","item.title")]))

write(f"{BASE}/speaking/topic_form.html", make_form("speaking","topic","Speaking Topic","scheduling:speaking_topic_list"))
write(f"{BASE}/speaking/pronunciation_form.html", make_form("speaking","pronunciation","Pronunciation","scheduling:pronunciation_list"))
write(f"{BASE}/speaking/roleplay_form.html", make_form("speaking","roleplay","Roleplay","scheduling:roleplay_list"))

print("\n✅ All list and form templates generated!")
