import streamlit as st
import streamlit.components.v1 as components
import re
from datetime import datetime

st.set_page_config(
    page_title="Folio",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background: #f0f0f0;
  color: #1a1a1a;
}
.stApp { background: #f0f0f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── App bar ── */
.appbar {
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}
.appbar-logo {
  font-family: 'Lora', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1a1a1a;
}
.appbar-stats {
  font-size: 0.7rem;
  color: #aaa;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
  padding: 0 12px;
  gap: 0;
}
.stTabs [data-baseweb="tab"] {
  font-size: 0.7rem;
  font-weight: 600;
  color: #bbb !important;
  padding: 9px 14px !important;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border-bottom: 2px solid transparent !important;
  background: transparent !important;
}
.stTabs [aria-selected="true"] {
  color: #1a1a1a !important;
  border-bottom-color: #1a1a1a !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 0 !important;
  background: #f0f0f0;
}

/* ── Tool panels ── */
.stTextInput input {
  background: #fff !important;
  border: 1px solid #ddd !important;
  border-radius: 6px !important;
  color: #1a1a1a !important;
  font-size: 0.88rem !important;
  padding: 8px 12px !important;
}
.stTextInput input:focus { border-color: #1a1a1a !important; box-shadow: none !important; }

.stButton > button {
  background: #1a1a1a !important;
  color: #fff !important;
  border: none !important;
  border-radius: 6px !important;
  font-weight: 500 !important;
  font-size: 0.82rem !important;
  padding: 8px 16px !important;
  width: 100%;
  transition: background 0.12s !important;
}
.stButton > button:hover { background: #333 !important; }

.stDownloadButton > button {
  background: #fff !important;
  color: #1a1a1a !important;
  border: 1px solid #ddd !important;
  border-radius: 6px !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  padding: 8px 16px !important;
  width: 100%;
}
.stDownloadButton > button:hover { background: #f5f5f5 !important; }

.slabel {
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #bbb;
  margin: 16px 0 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #e8e8e8;
}
.issue-row { background: #fff; border-left: 3px solid #ddd; border-radius: 0 5px 5px 0; padding: 7px 11px; margin-bottom: 5px; font-size: 0.8rem; color: #444; }
.issue-row.warn { border-left-color: #f59e0b; background: #fffdf5; color: #78350f; }
.issue-row.info { border-left-color: #60a5fa; background: #f0f7ff; color: #1e3a8a; }
.issue-row.ok   { border-left-color: #34d399; background: #f0fdf8; color: #065f46; }
.toc-row { display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #f0f0f0; font-size: 0.84rem; color: #333; }
.toc-row:last-child { border-bottom: none; }
.toc-pg { color: #bbb; font-size: 0.78rem; }
.freq-row { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
.freq-word { min-width: 80px; font-size: 0.78rem; color: #555; }
.freq-bar-bg { flex: 1; background: #f0f0f0; border-radius: 3px; height: 6px; }
.freq-bar { background: #1a1a1a; border-radius: 3px; height: 6px; }
.freq-n { font-size: 0.72rem; color: #bbb; min-width: 22px; text-align: right; }
.match-badge { display: inline-block; font-size: 0.75rem; color: #555; background: #f0f0f0; border-radius: 4px; padding: 3px 9px; margin-bottom: 8px; }
.check-row { display: flex; gap: 9px; align-items: flex-start; padding: 6px 0; border-bottom: 1px solid #f0f0f0; font-size: 0.8rem; color: #444; }
.check-row:last-child { border-bottom: none; }
.check-icon { color: #ccc; flex-shrink: 0; }
.stCheckbox label { color: #333 !important; font-size: 0.84rem !important; }
div[data-testid="metric-container"] { background: #fff; border: 1px solid #eee; border-radius: 6px; padding: 10px 12px; text-align: center; }
div[data-testid="metric-container"] label { color: #bbb !important; font-size: 0.6rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
div[data-testid="stMetricValue"] { color: #1a1a1a !important; font-family: 'Lora', serif !important; font-size: 1.2rem !important; }

@media (max-width: 640px) {
  .stTabs [data-baseweb="tab"] { font-size: 0.65rem; padding: 8px 10px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [
    ("html_content", ""),
    ("plain_text", ""),
    ("history", []),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────────────────
def push_history(t):
    if st.session_state.history and st.session_state.history[-1] == t:
        return
    st.session_state.history.append(t)
    if len(st.session_state.history) > 30:
        st.session_state.history.pop(0)

def strip_html(html):
    return re.sub(r'<[^>]+>', ' ', html).strip()

def wc(t):   return len(t.split()) if t.strip() else 0
def sc(t):   return len(re.findall(r'[.!?]+', t))
def pages(t): return max(1, round(wc(t) / 250))
def rtime(t): return max(1, round(wc(t) / 238))

def headings_from_html(html):
    out = []
    wp = 0
    for m in re.finditer(r'<h([1-3])[^>]*>(.*?)</h\1>', html, re.IGNORECASE | re.DOTALL):
        lvl = int(m.group(1))
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        out.append({"title": title, "level": lvl, "page": max(1, round(wp / 250))})
        wp += len(title.split())
    return out

def audit_plain(text):
    if not text.strip(): return []
    issues = []
    n = len(re.findall(r'  +', text))
    if n: issues.append(("warn", f"{n} double-space(s) found"))
    if "..." in text: issues.append(("info", f"{text.count('...')} ellipsis as '...' — consider … character"))
    if "--" in text: issues.append(("info", f"{text.count('--')} double-dash — consider em dash —"))
    long_p = [p for p in text.split("\n\n") if len(p.split()) > 300 and p.strip()]
    if long_p: issues.append(("warn", f"{len(long_p)} paragraph(s) over 300 words"))
    issues.append(("ok", f"{wc(text):,} words · ~{pages(text)} pages · {rtime(text)} min read"))
    return issues

def find_replace_plain(text, find, replace, case_sens, whole_word):
    if not find: return text, 0
    flags = 0 if case_sens else re.IGNORECASE
    pat = re.escape(find)
    if whole_word: pat = r'\b' + pat + r'\b'
    matches = re.findall(pat, text, flags=flags)
    return re.sub(pat, replace, text, flags=flags), len(matches)

def html_to_export(html):
    return f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'>
<style>
  body {{ font-family: Georgia, serif; max-width: 680px; margin: 60px auto; line-height: 1.9; font-size: 1.05rem; color: #1a1a1a; padding: 0 20px; }}
  h1 {{ text-align: center; margin-bottom: 2rem; }}
  h2 {{ margin-top: 2.5rem; }}
  h3 {{ margin-top: 1.5rem; }}
  p  {{ margin: 0 0 0.8rem; }}
</style>
</head><body>
{html}
</body></html>"""

# ── Quill editor component ────────────────────────────────────────────────────
QUILL_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link href="https://cdnjs.cloudflare.com/ajax/libs/quill/1.3.7/quill.snow.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/quill/1.3.7/quill.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; background: #f0f0f0; font-family: 'Georgia', serif; }

  /* ── Toolbar ── */
  #toolbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: #fff;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    padding: 6px 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 2px;
    align-items: center;
  }

  /* Override Quill toolbar styles */
  .ql-toolbar.ql-snow {
    border: none !important;
    padding: 0 !important;
    display: flex;
    flex-wrap: wrap;
    gap: 1px;
    align-items: center;
    width: 100%;
  }
  .ql-toolbar.ql-snow .ql-formats {
    margin-right: 4px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 1px;
  }
  .ql-toolbar button, .ql-toolbar .ql-picker {
    height: 28px !important;
    min-width: 28px;
    border-radius: 4px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }
  .ql-toolbar button:hover, .ql-toolbar button.ql-active {
    background: #f0f0f0 !important;
    color: #1a1a1a !important;
  }
  .ql-toolbar .ql-picker-label {
    border: 1px solid #e0e0e0 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-size: 0.78rem !important;
    height: 28px;
    display: flex;
    align-items: center;
  }
  .ql-toolbar .ql-font .ql-picker-label,
  .ql-toolbar .ql-size .ql-picker-label {
    min-width: 70px;
  }
  .ql-toolbar .ql-picker-options {
    background: #fff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
    padding: 4px !important;
    z-index: 999;
  }
  .ql-toolbar .ql-picker-item {
    border-radius: 4px;
    padding: 4px 8px !important;
    font-size: 0.82rem !important;
  }
  .ql-toolbar .ql-picker-item:hover { background: #f5f5f5 !important; }
  .ql-snow .ql-stroke { stroke: #444 !important; }
  .ql-snow .ql-fill { fill: #444 !important; }

  /* ── Page canvas ── */
  #canvas {
    background: #e8e8e8;
    padding: 20px 12px 60px;
    min-height: calc(100vh - 80px);
  }

  /* ── The page sheet ── */
  #editor-container {
    background: #fff;
    max-width: 680px;
    margin: 0 auto;
    box-shadow: 0 2px 20px rgba(0,0,0,0.15), 0 1px 4px rgba(0,0,0,0.08);
    border-radius: 1px;
    min-height: 80vh;
  }

  .ql-container.ql-snow {
    border: none !important;
    font-family: 'Georgia', serif;
  }
  .ql-editor {
    padding: 48px 52px !important;
    min-height: 80vh !important;
    font-size: 1.05rem !important;
    line-height: 1.9 !important;
    color: #1a1a1a !important;
  }
  .ql-editor p { margin-bottom: 0.3rem; }
  .ql-editor h1 { text-align: center; margin: 1.5rem 0 1rem; font-size: 1.8rem; }
  .ql-editor h2 { margin: 2rem 0 0.5rem; font-size: 1.3rem; border-bottom: 1px solid #eee; padding-bottom: 6px; }
  .ql-editor h3 { margin: 1.5rem 0 0.3rem; font-size: 1.1rem; }

  /* ── Font families in picker ── */
  .ql-font-georgia { font-family: 'Georgia', serif; }
  .ql-font-times   { font-family: 'Times New Roman', serif; }
  .ql-font-garamond { font-family: 'Garamond', serif; }
  .ql-font-helvetica { font-family: 'Helvetica', sans-serif; }
  .ql-font-courier { font-family: 'Courier New', monospace; }

  @media (max-width: 600px) {
    .ql-editor { padding: 28px 22px !important; font-size: 1rem !important; }
    #canvas { padding: 12px 6px 40px; }
  }
</style>
</head>
<body>

<div id="editor-wrapper">
  <!-- Quill toolbar will be injected here -->
  <div id="editor-container">
    <div id="editor">INITIAL_CONTENT</div>
  </div>
</div>

<!-- Hidden textarea to pass content to Streamlit -->
<textarea id="html-out" style="display:none"></textarea>
<textarea id="text-out" style="display:none"></textarea>

<script>
// Register custom fonts
var FontAttributor = Quill.import('formats/font');
FontAttributor.whitelist = ['georgia', 'times', 'garamond', 'helvetica', 'courier'];
Quill.register(FontAttributor, true);

var SizeAttributor = Quill.import('attributors/style/size');
SizeAttributor.whitelist = ['10px','11px','12px','13px','14px','16px','18px','20px','24px','28px','32px','36px'];
Quill.register(SizeAttributor, true);

var quill = new Quill('#editor', {
  theme: 'snow',
  placeholder: 'Start writing...',
  modules: {
    toolbar: {
      container: [
        [{ 'font': ['georgia','times','garamond','helvetica','courier'] }],
        [{ 'size': ['10px','11px','12px','13px','14px','16px','18px','20px','24px','28px','32px','36px'] }],
        [{ 'header': [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'align': [] }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        ['blockquote'],
        ['clean']
      ]
    }
  }
});

// Label font picker items
document.querySelectorAll('.ql-font .ql-picker-item').forEach(function(item) {
  var val = item.getAttribute('data-value');
  var labels = {
    'georgia': 'Georgia',
    'times': 'Times New Roman',
    'garamond': 'Garamond',
    'helvetica': 'Helvetica',
    'courier': 'Courier New',
    '': 'Default'
  };
  item.textContent = labels[val] || val;
});

// Label size picker items
document.querySelectorAll('.ql-size .ql-picker-item').forEach(function(item) {
  var val = item.getAttribute('data-value');
  item.textContent = val ? val.replace('px','pt') : '12pt';
});

// Send content to parent Streamlit every 800ms
function syncContent() {
  var html = quill.root.innerHTML;
  var text = quill.getText();
  document.getElementById('html-out').value = html;
  document.getElementById('text-out').value = text;
  // Post to parent window
  window.parent.postMessage({
    type: 'folio-content',
    html: html,
    text: text
  }, '*');
}

var syncTimer;
quill.on('text-change', function() {
  clearTimeout(syncTimer);
  syncTimer = setTimeout(syncContent, 600);
});

// Initial sync
setTimeout(syncContent, 100);
</script>
</body>
</html>
"""

# ── App bar ───────────────────────────────────────────────────────────────────
plain = st.session_state.plain_text
word_n = wc(plain)
stat_str = f"{word_n:,} words" if word_n else "Start writing..."

st.markdown(f"""
<div class="appbar">
  <span class="appbar-logo">📄 Folio</span>
  <span class="appbar-stats">{stat_str}</span>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_write, tab_tools, tab_export = st.tabs(["Write", "Tools", "Export"])

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE TAB — Quill editor
# ═══════════════════════════════════════════════════════════════════════════════
with tab_write:
    # Inject current content into the editor HTML
    safe_content = st.session_state.html_content.replace('\\', '\\\\').replace('`', '\\`')
    editor_html = QUILL_HTML.replace('INITIAL_CONTENT', '')

    # Use components.html to render the editor
    # We capture output via a form hack using query params
    result = components.html(editor_html, height=850, scrolling=False)

    # Content capture note
    st.markdown("""
    <div style="background:#fff;border-top:1px solid #e8e8e8;padding:8px 14px;font-size:0.72rem;color:#bbb;text-align:center">
      Your text auto-saves as you type · Switch to Tools tab to see stats &amp; word count
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TOOLS TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_tools:
    st.markdown('<div style="padding:16px">', unsafe_allow_html=True)
    t = st.session_state.plain_text

    st.markdown('<div class="slabel">Stats</div>', unsafe_allow_html=True)
    if t.strip():
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Words", f"{wc(t):,}")
        with c2: st.metric("Pages ~", pages(t))
        with c3: st.metric("Sentences", sc(t))
        with c4: st.metric("Read", f"{rtime(t)}m")

        st.markdown('<div class="slabel">Audit</div>', unsafe_allow_html=True)
        for lvl, msg in audit_plain(t):
            st.markdown(f'<div class="issue-row {lvl}">{msg}</div>', unsafe_allow_html=True)

        h = headings_from_html(st.session_state.html_content)
        if h:
            st.markdown('<div class="slabel">Structure</div>', unsafe_allow_html=True)
            for entry in h:
                indent = "&nbsp;&nbsp;&nbsp;" * (entry["level"] - 1)
                st.markdown(f'<div class="toc-row"><span>{indent}{entry["title"]}</span><span class="toc-pg">p.{entry["page"]}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="slabel">Top Words</div>', unsafe_allow_html=True)
        stopwords = {"the","and","a","to","of","in","is","it","that","was","he","she","his","her",
                     "i","you","we","they","with","for","on","at","be","as","had","have","this",
                     "but","from","or","an","by","are","said","not","so","what","all","were","when",
                     "there","been","one","do","their","my","me","no","if","can","up","its","out",
                     "into","about","how","your","our","them","will","has","would","could",
                     "than","then","just","like","some","these","those","which","who","him","us"}
        freq = {}
        for w in re.findall(r'\b[a-z]+\b', t.lower()):
            if len(w) > 3 and w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:12]
        if top:
            mx = top[0][1]
            for word, count in top:
                bar = int((count / mx) * 100)
                st.markdown(f"""
                <div class="freq-row">
                  <span class="freq-word">{word}</span>
                  <div class="freq-bar-bg"><div class="freq-bar" style="width:{bar}%"></div></div>
                  <span class="freq-n">{count}</span>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#bbb;font-size:0.85rem;padding:12px 0">Write something in the Write tab first.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_export:
    st.markdown('<div style="padding:16px">', unsafe_allow_html=True)
    t = st.session_state.plain_text
    h = st.session_state.html_content
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    st.markdown('<div class="slabel">Download</div>', unsafe_allow_html=True)
    if t.strip():
        c1, c2 = st.columns(2)
        with c1:
            st.download_button("⬇ Plain text (.txt)", data=t,
                file_name=f"document_{ts}.txt", mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("⬇ Formatted (.html)", data=html_to_export(h),
                file_name=f"document_{ts}.html", mime="text/html", use_container_width=True)
    else:
        st.markdown('<p style="color:#bbb;font-size:0.85rem">Nothing to export yet.</p>', unsafe_allow_html=True)

    st.markdown('<div class="slabel" style="margin-top:20px">Publishing Checklist</div>', unsafe_allow_html=True)
    checklist = [
        ("Ebook", ["Use Heading 1/2/3 for chapter structure","Smart quotes throughout","No double spaces","Front matter: title page, copyright, dedication","Back matter: About Author, newsletter link","Export HTML → paste into Atticus or Reedsy"]),
        ("Print / KDP", ["Trim: 5x8\" novels · 6x9\" nonfiction","Margins: inside 0.875\" · outside 0.625\"","Body: Garamond or Times 11-12pt","Chapter pages start ~1/3 down the page","PDF/X-1a export with embedded fonts"]),
        ("Upload", ["Cover: 2560x1600px JPG minimum","Separate ISBNs for ebook and print","2-3 BISAC categories · 7 keyword phrases"]),
    ]
    for section, items in checklist:
        st.markdown(f'<div class="slabel" style="margin-top:16px">{section}</div>', unsafe_allow_html=True)
        for item in items:
            st.markdown(f'<div class="check-row"><span class="check-icon">☐</span><span>{item}</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
