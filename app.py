import streamlit as st
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
  background: #fafafa;
  color: #1a1a1a;
}
.stApp { background: #fafafa; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Toolbar strip ── */
.toolbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.toolbar-title {
  font-family: 'Lora', serif;
  font-size: 1rem;
  color: #1a1a1a;
  font-weight: 600;
  white-space: nowrap;
}
.toolbar-stats {
  font-size: 0.72rem;
  color: #aaa;
  white-space: nowrap;
}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  padding: 0 16px;
  gap: 0;
}
.stTabs [data-baseweb="tab"] {
  font-size: 0.72rem;
  font-weight: 500;
  color: #bbb !important;
  padding: 10px 14px !important;
  letter-spacing: 0.05em;
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
  background: #fafafa;
}

/* ── The writing area — this is the hero ── */
.stTextArea textarea {
  background: #fff !important;
  border: none !important;
  border-radius: 0 !important;
  color: #1a1a1a !important;
  font-family: 'Lora', serif !important;
  font-size: 1.05rem !important;
  line-height: 1.9 !important;
  padding: 32px 24px !important;
  resize: none !important;
  box-shadow: none !important;
  min-height: 80vh !important;
  width: 100% !important;
}
.stTextArea textarea:focus {
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}
.stTextArea { border: none !important; }
div[data-baseweb="textarea"] { border: none !important; box-shadow: none !important; }

/* ── Tool panels (non-editor tabs) ── */
.panel {
  padding: 20px 16px;
  background: #fafafa;
  min-height: 60vh;
}

/* ── Inputs in panels ── */
.stTextInput input {
  background: #fff !important;
  border: 1px solid #ddd !important;
  border-radius: 6px !important;
  color: #1a1a1a !important;
  font-size: 0.9rem !important;
  padding: 8px 12px !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus {
  border-color: #1a1a1a !important;
  box-shadow: none !important;
}

/* ── Buttons ── */
.stButton > button {
  background: #1a1a1a !important;
  color: #fff !important;
  border: none !important;
  border-radius: 6px !important;
  font-family: 'Inter', sans-serif !important;
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
.stDownloadButton > button:hover { background: #f5f5f5 !important; border-color: #aaa !important; }

/* ── Stat pills ── */
.stat-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  padding: 10px 16px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}
.stat-pill {
  font-size: 0.7rem;
  color: #888;
  background: #f5f5f5;
  border-radius: 20px;
  padding: 3px 10px;
  white-space: nowrap;
}
.stat-pill b { color: #1a1a1a; font-weight: 600; }

/* ── Section label ── */
.slabel {
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #bbb;
  margin: 16px 0 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #eee;
}

/* ── Issue rows ── */
.issue-row {
  background: #fff;
  border-left: 3px solid #ddd;
  border-radius: 0 5px 5px 0;
  padding: 7px 11px;
  margin-bottom: 5px;
  font-size: 0.8rem;
  color: #444;
}
.issue-row.warn { border-left-color: #f59e0b; background: #fffdf5; color: #78350f; }
.issue-row.info { border-left-color: #60a5fa; background: #f0f7ff; color: #1e3a8a; }
.issue-row.ok   { border-left-color: #34d399; background: #f0fdf8; color: #065f46; }

/* ── TOC ── */
.toc-row {
  display: flex;
  justify-content: space-between;
  padding: 7px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.84rem;
  color: #333;
}
.toc-row:last-child { border-bottom: none; }
.toc-pg { color: #bbb; font-size: 0.78rem; }

/* ── Word freq bar ── */
.freq-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}
.freq-word { min-width: 80px; font-size: 0.78rem; color: #555; }
.freq-bar-bg { flex: 1; background: #f0f0f0; border-radius: 3px; height: 6px; }
.freq-bar { background: #1a1a1a; border-radius: 3px; height: 6px; }
.freq-n { font-size: 0.72rem; color: #bbb; min-width: 22px; text-align: right; }

/* ── Match badge ── */
.match-badge {
  display: inline-block;
  font-size: 0.75rem;
  color: #555;
  background: #f0f0f0;
  border-radius: 4px;
  padding: 3px 9px;
  margin-bottom: 8px;
}

/* ── Checklist ── */
.check-row {
  display: flex;
  gap: 9px;
  align-items: flex-start;
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.8rem;
  color: #444;
}
.check-row:last-child { border-bottom: none; }
.check-icon { color: #ccc; flex-shrink: 0; margin-top: 1px; }

/* ── Checkbox / radio labels ── */
.stCheckbox label { color: #333 !important; font-size: 0.84rem !important; }
.stRadio label { color: #333 !important; font-size: 0.84rem !important; }

/* ── Page preview ── */
.preview-page {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  padding: 40px 32px;
  font-family: 'Lora', serif;
  font-size: 1rem;
  line-height: 1.95;
  color: #1a1a1a;
  max-height: 70vh;
  overflow-y: auto;
  box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 10px 12px;
  text-align: center;
}
div[data-testid="metric-container"] label {
  color: #bbb !important;
  font-size: 0.6rem !important;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
div[data-testid="stMetricValue"] {
  color: #1a1a1a !important;
  font-family: 'Lora', serif !important;
  font-size: 1.2rem !important;
}

@media (max-width: 640px) {
  .stTextArea textarea { font-size: 1rem !important; padding: 20px 16px !important; }
  .preview-page { padding: 24px 18px; font-size: 0.95rem; }
  .stTabs [data-baseweb="tab"] { font-size: 0.68rem; padding: 9px 10px !important; }
}

/* ── Page view ── */
.page-canvas {
  background: #e8e8e8;
  padding: 24px 16px 40px;
  min-height: 90vh;
}
.page-sheet {
  background: #fff;
  width: 100%;
  max-width: 680px;
  margin: 0 auto;
  padding: 52px 48px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.13), 0 1px 4px rgba(0,0,0,0.08);
  border-radius: 1px;
  font-family: 'Lora', serif;
  font-size: 1.05rem;
  line-height: 1.95;
  color: #1a1a1a;
  min-height: 90vh;
  white-space: pre-wrap;
  word-break: break-word;
  cursor: text;
}
.page-sheet h1 { font-size: 1.5rem; text-align: center; margin: 1.5rem 0 2rem; font-weight: 600; }
.page-sheet h2 { font-size: 1.1rem; margin: 2.2rem 0 0.5rem; font-weight: 600; border-bottom: 1px solid #eee; padding-bottom: 5px; }
.page-sheet h3 { font-size: 0.95rem; margin: 1.5rem 0 0.3rem; font-weight: 600; }
.page-sheet p  { margin: 0 0 0.1rem 1.4em; }
.page-sheet .scene { text-align: center; color: #aaa; letter-spacing: 0.4em; margin: 1.5rem 0; font-size: 0.85rem; }
.view-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 6px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  font-size: 0.75rem;
  color: #555;
  cursor: pointer;
  white-space: nowrap;
}
.view-toggle.active {
  background: #1a1a1a;
  color: #fff;
  border-color: #1a1a1a;
}
@media (max-width: 640px) {
  .page-sheet { padding: 36px 24px; font-size: 1rem; }
  .page-canvas { padding: 16px 10px 32px; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("text", ""), ("history", []), ("doc_title", "Untitled Document"), ("page_view", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────────────────
def push_history(t):
    if st.session_state.history and st.session_state.history[-1] == t:
        return
    st.session_state.history.append(t)
    if len(st.session_state.history) > 30:
        st.session_state.history.pop(0)

def wc(t): return len(t.split()) if t.strip() else 0
def sc(t): return len(re.findall(r'[.!?]+', t))
def pc(t): return len([p for p in t.split("\n\n") if p.strip()])
def pages(t): return max(1, round(wc(t) / 250))
def read_time(t): return max(1, round(wc(t) / 238))

def headings(text):
    out = []
    wp = 0
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r'^#{1,3}\s+', s):
            lvl = len(re.match(r'^(#+)', s).group(1))
            title = re.sub(r'^#+\s+', '', s)
            out.append({"title": title, "level": lvl, "page": max(1, round(wp/250))})
        elif re.match(r'(?i)^chapter\s+', s):
            out.append({"title": s, "level": 2, "page": max(1, round(wp/250))})
        wp += len(line.split())
    return out

def audit(text):
    if not text.strip():
        return []
    issues = []
    n = len(re.findall(r'  +', text))
    if n: issues.append(("warn", f"{n} double-space(s) found"))
    n = len(re.findall(r'"', text))
    if n: issues.append(("warn", f"{n} straight double-quote(s) — consider smart quotes"))
    if "..." in text: issues.append(("info", f"{text.count('...')} ellipsis as '...' — consider … character"))
    if "--" in text: issues.append(("info", f"{text.count('--')} double-dash — consider em dash —"))
    n = sum(1 for l in text.split("\n") if l != l.rstrip())
    if n: issues.append(("info", f"{n} line(s) with trailing whitespace"))
    if re.search(r'\n{3,}', text): issues.append(("warn", "3+ consecutive blank lines found"))
    long_p = [p for p in text.split("\n\n") if len(p.split()) > 300 and p.strip()]
    if long_p: issues.append(("warn", f"{len(long_p)} paragraph(s) over 300 words"))
    h = headings(text)
    if h:
        issues.append(("ok", f"{len(h)} heading(s) detected"))
    else:
        issues.append(("info", "No headings found — use # Title or ## Chapter Name"))
    issues.append(("ok", f"{wc(text):,} words · ~{pages(text)} pages · {read_time(text)} min read"))
    return issues

def do_format(text, opts):
    if opts.get("double_space"):
        text = re.sub(r'  +', ' ', text)
    if opts.get("smart_quotes"):
        text = re.sub(r'"(\S)', '\u201c\\1', text)
        text = re.sub(r'(\S)"', '\\1\u201d', text)
        text = re.sub(r'"', '\u201d', text)
        text = re.sub(r"'(\S)", '\u2018\\1', text)
        text = re.sub(r"(\S)'", '\\1\u2019', text)
        text = re.sub(r"'", '\u2019', text)
    if opts.get("ellipsis"):
        text = re.sub(r'\.{4}', '\u2026', text)
        text = re.sub(r'\.{3}', '\u2026', text)
    if opts.get("em_dash"):
        text = re.sub(r'\s*---\s*', '\u2014', text)
        text = re.sub(r'\s*--\s*', '\u2014', text)
    if opts.get("strip_trailing"):
        text = "\n".join(l.rstrip() for l in text.split("\n"))
    if opts.get("blank_lines"):
        text = re.sub(r'\n{3,}', '\n\n', text)
    if opts.get("scene_break"):
        text = re.sub(r'(?m)^\s*[\*\-]{3,}\s*$', '***', text)
    return text

def find_replace(text, find, replace, case_sens, whole_word):
    if not find: return text, 0
    flags = 0 if case_sens else re.IGNORECASE
    pat = re.escape(find)
    if whole_word: pat = r'\b' + pat + r'\b'
    matches = re.findall(pat, text, flags=flags)
    return re.sub(pat, replace, text, flags=flags), len(matches)

def to_html(text):
    lines = text.split("\n")
    out = ["""<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>body{font-family:Georgia,serif;max-width:640px;margin:60px auto;line-height:1.9;font-size:1.05rem;color:#1a1a1a}
h1{text-align:center;margin-bottom:2rem}h2{margin-top:2.5rem}h3{margin-top:1.5rem}
p{margin:0 0 0.8rem 1.3em}.scene{text-align:center;color:#aaa;letter-spacing:0.3em;margin:1.5rem 0}
</style></head><body>"""]
    for line in lines:
        s = line.strip()
        if not s: continue
        if re.match(r'^###\s+', s):   out.append(f"<h3>{re.sub(r'^###\\s+','',s)}</h3>")
        elif re.match(r'^##\s+', s):  out.append(f"<h2>{re.sub(r'^##\\s+','',s)}</h2>")
        elif re.match(r'^#\s+', s):   out.append(f"<h1>{re.sub(r'^#\\s+','',s)}</h1>")
        elif s == "***": out.append('<div class="scene">* * *</div>')
        else: out.append(f"<p>{s}</p>")
    out.append("</body></html>")
    return "\n".join(out)

# ── Toolbar ───────────────────────────────────────────────────────────────────
t = st.session_state.text
word_n = wc(t)
stat_str = f"{word_n:,} words" if word_n else "Start typing..."

st.markdown(f"""
<div class="toolbar">
  <span class="toolbar-title">📄 Folio</span>
  <span class="toolbar-stats">{stat_str}</span>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_write, tab_tools, tab_preview, tab_export = st.tabs([
    "Write", "Tools", "Preview", "Export"
])

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE TAB — just the document, nothing else
# ═══════════════════════════════════════════════════════════════════════════════
with tab_write:
    # ── View toggle ──
    tcol1, tcol2 = st.columns([3, 1])
    with tcol2:
        pv_label = "📄 Page view" if not st.session_state.page_view else "✏️ Edit mode"
        if st.button(pv_label, use_container_width=True, key="pv_toggle"):
            st.session_state.page_view = not st.session_state.page_view
            st.rerun()

    if not st.session_state.page_view:
        # ── Raw editor ──
        new_text = st.text_area(
            "editor",
            value=st.session_state.text,
            placeholder="Start writing...",
            height=700,
            label_visibility="collapsed",
            key="main_editor",
        )
        if new_text != st.session_state.text:
            push_history(st.session_state.text)
            st.session_state.text = new_text
    else:
        # ── Page view (read/review mode) ──
        parts = []
        for line in st.session_state.text.split("\n"):
            s = line.strip()
            if not s:
                parts.append('<div style="height:0.65rem"></div>')
            elif re.match(r'^###\s+', s):
                h = re.sub(r'^###\s+', '', s)
                parts.append(f'<h3>{h}</h3>')
            elif re.match(r'^##\s+', s):
                h = re.sub(r'^##\s+', '', s)
                parts.append(f'<h2>{h}</h2>')
            elif re.match(r'^#\s+', s):
                h = re.sub(r'^#\s+', '', s)
                parts.append(f'<h1>{h}</h1>')
            elif s == "***":
                parts.append('<div class="scene">* * *</div>')
            else:
                parts.append(f'<p>{s}</p>')
        page_html = "".join(parts) if parts else '<span style="color:#ccc;font-style:italic">Start writing to see the page view...</span>'
        st.markdown(f'''
        <div class="page-canvas">
          <div class="page-sheet">{page_html}</div>
        </div>''', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TOOLS TAB — stats, find/replace, format, audit
# ═══════════════════════════════════════════════════════════════════════════════
with tab_tools:
    t = st.session_state.text

    # ── Stats ──
    st.markdown('<div class="slabel">Document Stats</div>', unsafe_allow_html=True)
    if t.strip():
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Words", f"{wc(t):,}")
        with c2: st.metric("Pages ~", pages(t))
        with c3: st.metric("Sentences", sc(t))
        with c4: st.metric("Read", f"{read_time(t)}m")
    else:
        st.markdown('<p style="color:#bbb;font-size:0.85rem;padding:8px 0">Nothing written yet.</p>', unsafe_allow_html=True)

    # ── Undo / Clear ──
    st.markdown('<div class="slabel">History</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        if st.button("↩ Undo", use_container_width=True):
            if st.session_state.history:
                st.session_state.text = st.session_state.history.pop()
                st.rerun()
            else:
                st.toast("Nothing to undo")
    with cb:
        if st.button("🗑 Clear document", use_container_width=True):
            if st.session_state.text:
                push_history(st.session_state.text)
                st.session_state.text = ""
                st.rerun()

    # ── Find & Replace ──
    st.markdown('<div class="slabel">Find & Replace</div>', unsafe_allow_html=True)
    find_str = st.text_input("Find", placeholder='e.g. "said"', label_visibility="collapsed", key="find_in")
    repl_str = st.text_input("Replace with", placeholder='e.g. "whispered"', label_visibility="collapsed", key="repl_in")
    fc1, fc2 = st.columns(2)
    with fc1: case_s = st.checkbox("Case sensitive", key="case_cb")
    with fc2: whole_w = st.checkbox("Whole word", key="whole_cb")

    if find_str and t:
        try:
            flags = 0 if case_s else re.IGNORECASE
            pat = (r'\b' + re.escape(find_str) + r'\b') if whole_w else re.escape(find_str)
            n = len(re.findall(pat, t, flags=flags))
            st.markdown(f'<span class="match-badge">{n} match{"es" if n!=1 else ""}</span>', unsafe_allow_html=True)
        except: pass

    ra, rb = st.columns(2)
    with ra:
        if st.button("Replace All", use_container_width=True, key="rep_btn"):
            if find_str and t:
                push_history(t)
                new_t, n = find_replace(t, find_str, repl_str, case_s, whole_w)
                st.session_state.text = new_t
                st.toast(f"Replaced {n} occurrence(s)")
                st.rerun()
    with rb:
        if st.button("↩ Undo replace", use_container_width=True, key="rep_undo"):
            if st.session_state.history:
                st.session_state.text = st.session_state.history.pop()
                st.rerun()

    # ── Auto-format ──
    st.markdown('<div class="slabel">Auto-Format</div>', unsafe_allow_html=True)
    opts = {}
    opts["double_space"]   = st.checkbox("Remove double spaces",           value=True,  key="f1")
    opts["blank_lines"]    = st.checkbox("Collapse extra blank lines",     value=True,  key="f2")
    opts["strip_trailing"] = st.checkbox("Strip trailing whitespace",      value=True,  key="f3")
    opts["smart_quotes"]   = st.checkbox("Straighten → smart quotes",      value=False, key="f4")
    opts["ellipsis"]       = st.checkbox("... → … ellipsis",              value=False, key="f5")
    opts["em_dash"]        = st.checkbox("-- → — em dash",                value=False, key="f6")
    opts["scene_break"]    = st.checkbox("Normalize scene breaks to ***",  value=False, key="f7")

    fa, fb = st.columns(2)
    with fa:
        if st.button("Apply Formatting", use_container_width=True, key="fmt_btn"):
            if t:
                push_history(t)
                st.session_state.text = do_format(t, opts)
                st.toast("Formatting applied")
                st.rerun()
    with fb:
        if st.button("↩ Undo", use_container_width=True, key="fmt_undo"):
            if st.session_state.history:
                st.session_state.text = st.session_state.history.pop()
                st.rerun()

    # ── Audit ──
    if t.strip():
        st.markdown('<div class="slabel">Document Audit</div>', unsafe_allow_html=True)
        for lvl, msg in audit(t):
            st.markdown(f'<div class="issue-row {lvl}">{msg}</div>', unsafe_allow_html=True)

        # TOC
        h = headings(t)
        if h:
            st.markdown('<div class="slabel">Structure</div>', unsafe_allow_html=True)
            for entry in h:
                indent = "&nbsp;&nbsp;&nbsp;" * (entry["level"] - 1)
                st.markdown(f"""
                <div class="toc-row">
                  <span>{indent}{entry['title']}</span>
                  <span class="toc-pg">p.{entry['page']}</span>
                </div>""", unsafe_allow_html=True)

        # Word freq
        st.markdown('<div class="slabel">Top Words</div>', unsafe_allow_html=True)
        stopwords = {"the","and","a","to","of","in","is","it","that","was","he","she","his","her",
                     "i","you","we","they","with","for","on","at","be","as","had","have","this",
                     "but","from","or","an","by","are","said","not","so","what","all","were","when",
                     "there","been","one","do","their","my","me","no","if","can","up","its","out",
                     "into","about","more","how","your","our","them","will","has","would","could",
                     "than","then","just","like","some","these","those","which","who","him","us",
                     "did","she","her","him","its","been","were","they","have","this","with","that"}
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

# ═══════════════════════════════════════════════════════════════════════════════
# PREVIEW TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_preview:
    t = st.session_state.text
    st.markdown('<div style="padding: 16px 16px 8px">', unsafe_allow_html=True)
    if not t.strip():
        st.markdown('<p style="color:#bbb;font-size:0.9rem;padding:20px 0">Nothing to preview yet.</p>', unsafe_allow_html=True)
    else:
        parts = []
        for line in t.split("\n"):
            s = line.strip()
            if not s:
                parts.append('<div style="height:0.7rem"></div>')
            elif re.match(r'^###\s+', s):
                h = re.sub(r'^###\s+', '', s)
                parts.append(f'<h3 style="font-size:1rem;margin:1.5rem 0 0.3rem;font-weight:600">{h}</h3>')
            elif re.match(r'^##\s+', s):
                h = re.sub(r'^##\s+', '', s)
                parts.append(f'<h2 style="font-size:1.15rem;margin:2rem 0 0.4rem;font-weight:600;border-bottom:1px solid #eee;padding-bottom:6px">{h}</h2>')
            elif re.match(r'^#\s+', s):
                h = re.sub(r'^#\s+', '', s)
                parts.append(f'<h1 style="font-size:1.5rem;text-align:center;margin:1.5rem 0 1rem;font-weight:600">{h}</h1>')
            elif s == "***":
                parts.append('<div style="text-align:center;color:#ccc;letter-spacing:0.4em;margin:1.5rem 0;font-size:0.85rem">* * *</div>')
            else:
                parts.append(f'<p style="margin:0 0 0.1rem 1.3em;text-indent:0">{s}</p>')
        st.markdown(f'<div class="preview-page">{"".join(parts)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT TAB
# ═══════════════════════════════════════════════════════════════════════════════
with tab_export:
    t = st.session_state.text
    st.markdown('<div style="padding:16px">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">Download</div>', unsafe_allow_html=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    if t.strip():
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("⬇ .txt", data=t,
                file_name=f"document_{ts}.txt", mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("⬇ .md", data=t,
                file_name=f"document_{ts}.md", mime="text/markdown", use_container_width=True)
        with c3:
            st.download_button("⬇ .html", data=to_html(t),
                file_name=f"document_{ts}.html", mime="text/html", use_container_width=True)
    else:
        st.markdown('<p style="color:#bbb;font-size:0.85rem">Nothing written yet.</p>', unsafe_allow_html=True)

    st.markdown('<div class="slabel" style="margin-top:24px">Publishing Checklist</div>', unsafe_allow_html=True)
    checklist = [
        ("Ebook prep", [
            "Headings use # / ## / ### format for TOC generation",
            "Scene breaks are *** on their own line",
            "Smart quotes used throughout (not straight quotes)",
            "No double spaces or tab indents",
            "Front matter: title page, copyright, dedication",
            "Back matter: About the Author, newsletter link",
            "Paste .md into Atticus, Reedsy, or Kindle Create",
        ]),
        ("Print / KDP", [
            "Trim size: 5x8\" novels · 6x9\" nonfiction · 5.5x8.5\" general",
            "Margins: inside 0.875\" · outside 0.625\" · top/bottom 0.75\"",
            "Body font: Garamond or Times 11-12pt · 1.2-1.4x line spacing",
            "Chapter pages start ~1/3 down · no page number on those pages",
            "Fonts embedded before PDF export · export as PDF/X-1a",
            "Check for widows and orphans before final export",
        ]),
        ("Uploading", [
            "Cover: 2560x1600px minimum, JPG or TIFF",
            "Separate ISBNs for ebook and print",
            "2-3 BISAC categories selected",
            "7 keyword phrases (not single words)",
            "Description previewed in KDP before publishing",
        ]),
    ]
    for section, items in checklist:
        st.markdown(f'<div class="slabel" style="margin-top:18px">{section}</div>', unsafe_allow_html=True)
        for item in items:
            st.markdown(f'<div class="check-row"><span class="check-icon">☐</span><span>{item}</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
