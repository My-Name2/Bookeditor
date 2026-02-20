import streamlit as st
import re
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Folio — Manuscript Editor",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #fff; color: #1a1a1a; }
  .stApp { background: #fff; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  .topbar { background: #fff; border-bottom: 2px solid #1a1a1a; padding: 12px 18px; display: flex; align-items: center; gap: 10px; }
  .topbar-logo { font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #1a1a1a; }
  .topbar-sub { font-size: 0.68rem; color: #999; letter-spacing: 0.12em; text-transform: uppercase; }

  .stTabs [data-baseweb="tab-list"] { background: #f6f6f6; border-bottom: 1px solid #ddd; padding: 0 10px; gap: 0; }
  .stTabs [data-baseweb="tab"] { font-size: 0.74rem; font-weight: 600; color: #aaa !important; padding: 11px 12px !important; letter-spacing: 0.06em; text-transform: uppercase; border-bottom: 2px solid transparent !important; background: transparent !important; }
  .stTabs [aria-selected="true"] { color: #1a1a1a !important; border-bottom-color: #1a1a1a !important; }
  .stTabs [data-baseweb="tab-panel"] { padding: 18px 14px !important; background: #fff; }

  .stTextArea textarea { background: #fff !important; border: 1px solid #ccc !important; border-radius: 8px !important; color: #1a1a1a !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.93rem !important; line-height: 1.8 !important; padding: 14px !important; resize: vertical; }
  .stTextArea textarea:focus { border-color: #1a1a1a !important; box-shadow: 0 0 0 2px rgba(26,26,26,0.08) !important; }
  .stTextInput input { background: #fff !important; border: 1px solid #ccc !important; border-radius: 8px !important; color: #1a1a1a !important; font-size: 0.88rem !important; padding: 8px 12px !important; }
  .stTextInput input:focus { border-color: #1a1a1a !important; }

  .stButton > button { background: #1a1a1a !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 0.82rem !important; letter-spacing: 0.04em !important; padding: 9px 16px !important; width: 100%; transition: background 0.15s !important; }
  .stButton > button:hover { background: #333 !important; }

  div[data-testid="metric-container"] { background: #f6f6f6; border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px 12px; text-align: center; }
  div[data-testid="metric-container"] label { color: #999 !important; font-size: 0.65rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
  div[data-testid="stMetricValue"] { color: #1a1a1a !important; font-family: 'Playfair Display', serif !important; font-size: 1.25rem !important; }

  .card { background: #f9f9f9; border: 1px solid #e0e0e0; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; }
  .card-title { font-family: 'Playfair Display', serif; font-size: 0.95rem; color: #1a1a1a; margin-bottom: 6px; }
  .card-body { font-size: 0.8rem; color: #555; line-height: 1.65; }

  .slabel { font-size: 0.62rem; letter-spacing: 0.14em; text-transform: uppercase; color: #bbb; margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid #eee; }

  .page-preview { background: #fff; color: #1a1a1a; border-radius: 8px; padding: 36px 32px; font-family: 'Playfair Display', serif; font-size: 1rem; line-height: 2; white-space: pre-wrap; word-break: break-word; border: 1px solid #ddd; max-height: 540px; overflow-y: auto; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }

  .toc-entry { display: flex; justify-content: space-between; align-items: baseline; padding: 7px 0; border-bottom: 1px dotted #ddd; font-size: 0.85rem; }
  .toc-entry:last-child { border-bottom: none; }
  .toc-title { color: #1a1a1a; }
  .toc-page { color: #999; font-family: 'Playfair Display', serif; font-size: 0.9rem; }

  .issue-row { background: #f9f9f9; border-left: 3px solid #1a1a1a; border-radius: 0 6px 6px 0; padding: 8px 12px; margin-bottom: 6px; font-size: 0.82rem; color: #333; }
  .issue-row.warn { border-left-color: #d97706; background: #fffbf0; color: #92400e; }
  .issue-row.info { border-left-color: #2563eb; background: #eff6ff; color: #1e40af; }
  .issue-row.ok   { border-left-color: #16a34a; background: #f0fdf4; color: #166534; }

  .stDownloadButton > button { background: #f6f6f6 !important; color: #1a1a1a !important; border: 1px solid #ccc !important; font-size: 0.8rem !important; }
  .stDownloadButton > button:hover { background: #eee !important; border-color: #1a1a1a !important; }

  .stCheckbox label { color: #1a1a1a !important; font-size: 0.84rem !important; }
  .stRadio label { color: #1a1a1a !important; font-size: 0.84rem !important; }

  .match-count { font-size: 0.78rem; color: #1a1a1a; padding: 4px 10px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 4px; display: inline-block; margin-bottom: 8px; }

  @media (max-width: 640px) {
    .topbar { padding: 10px 12px; }
    .topbar-logo { font-size: 1.1rem; }
    .stTabs [data-baseweb="tab"] { font-size: 0.68rem; padding: 9px 7px !important; }
    .stTabs [data-baseweb="tab-panel"] { padding: 12px 10px !important; }
    .page-preview { padding: 24px 18px; font-size: 0.9rem; }
  }
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div>
    <div class="topbar-logo">📖 Folio</div>
    <div class="topbar-sub">Manuscript Editor</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "manuscript" not in st.session_state:
    st.session_state.manuscript = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "notes" not in st.session_state:
    st.session_state.notes = ""

# ── Helpers ───────────────────────────────────────────────────────────────────

def push_history(text: str):
    if st.session_state.history and st.session_state.history[-1] == text:
        return
    st.session_state.history.append(text)
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

def word_count(text):
    return len(text.split()) if text.strip() else 0

def sentence_count(text):
    return len(re.findall(r'[.!?]+', text))

def paragraph_count(text):
    return len([p for p in text.split("\n\n") if p.strip()])

def detect_chapters(text):
    chapters = []
    word_pos = 0
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r'^##\s+', s):
            chapters.append({"title": re.sub(r'^##\s+', '', s), "word_offset": word_pos})
        elif re.match(r'(?i)^chapter\s+', s):
            chapters.append({"title": s, "word_offset": word_pos})
        word_pos += len(line.split())
    return chapters

def build_toc(text):
    toc = []
    word_pos = 0
    for line in text.split("\n"):
        s = line.strip()
        title = None
        if re.match(r'^##\s+', s):
            title = re.sub(r'^##\s+', '', s)
        elif re.match(r'(?i)^chapter\s+', s):
            title = s
        if title:
            toc.append({"title": title, "page": max(1, round(word_pos / 250))})
        word_pos += len(line.split())
    return toc

def audit_text(text):
    issues = []
    if not text.strip():
        return issues
    if "  " in text:
        issues.append({"level": "warn", "msg": f"{len(re.findall(r'  +', text))} double-space occurrence(s)"})
    dq = len(re.findall(r'"', text))
    if dq:
        issues.append({"level": "warn", "msg": f"{dq} straight double-quote(s) — consider smart quotes"})
    if "..." in text:
        issues.append({"level": "info", "msg": f"{text.count('...')} '...' found — consider ellipsis character (…)"})
    if "--" in text:
        issues.append({"level": "info", "msg": f"{text.count('--')} '--' found — consider em dash (—)"})
    trailing = sum(1 for l in text.split("\n") if l != l.rstrip())
    if trailing:
        issues.append({"level": "info", "msg": f"{trailing} line(s) with trailing whitespace"})
    if re.search(r'\n{3,}', text):
        issues.append({"level": "warn", "msg": "3+ consecutive blank lines detected"})
    long_paras = [p for p in text.split("\n\n") if len(p.split()) > 300 and p.strip()]
    if long_paras:
        issues.append({"level": "warn", "msg": f"{len(long_paras)} paragraph(s) over 300 words — consider splitting"})
    chapters = detect_chapters(text)
    if not chapters:
        issues.append({"level": "warn", "msg": "No chapter headings found — use '## Chapter 1: Title' format"})
    else:
        issues.append({"level": "ok", "msg": f"{len(chapters)} chapter heading(s) detected ✓"})
    wc = word_count(text)
    issues.append({"level": "ok" if wc >= 1000 else "info", "msg": f"{wc:,} words total"})
    return issues

def auto_format(text, opts):
    if opts.get("double_space"):
        text = re.sub(r'  +', ' ', text)
    if opts.get("smart_quotes"):
        # Double quotes: open = \u201c, close = \u201d
        text = re.sub(r'"(\S)', '\u201c\\1', text)
        text = re.sub(r'(\S)"', '\\1\u201d', text)
        text = re.sub(r'"', '\u201d', text)
        # Single quotes / apostrophes: open = \u2018, close = \u2019
        text = re.sub(r"'(\S)", '\u2018\\1', text)
        text = re.sub(r"(\S)'", '\\1\u2019', text)
        text = re.sub(r"'", '\u2019', text)
    if opts.get("ellipsis"):
        text = re.sub(r'\.{4}', '…', text)
        text = re.sub(r'\.{3}', '…', text)
    if opts.get("em_dash"):
        text = re.sub(r'\s*---\s*', '—', text)
        text = re.sub(r'\s*--\s*', '—', text)
    if opts.get("strip_trailing"):
        text = "\n".join(l.rstrip() for l in text.split("\n"))
    if opts.get("blank_lines"):
        text = re.sub(r'\n{3,}', '\n\n', text)
    if opts.get("scene_break"):
        text = re.sub(r'(?m)^\s*[\*\-]{3,}\s*$', '***', text)
    if opts.get("chapter_headings"):
        text = re.sub(r'(?im)^chapter\s+(\w+)\s*$', lambda m: f"## Chapter {m.group(1)}", text)
    return text

def find_replace(text, find, replace, case_sensitive, whole_word):
    if not find:
        return text, 0
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.escape(find)
    if whole_word:
        pattern = r'\b' + pattern + r'\b'
    matches = re.findall(pattern, text, flags=flags)
    return re.sub(pattern, replace, text, flags=flags), len(matches)

def export_html(text):
    lines = text.split("\n")
    html = ["<!DOCTYPE html><html><head><meta charset='utf-8'>",
            "<style>body{font-family:Georgia,serif;max-width:660px;margin:60px auto;line-height:1.9;font-size:1.05rem;color:#1a1a1a}",
            "h1{text-align:center;margin-bottom:2rem}h2{margin-top:2.5rem}p{margin:0 0 0.8rem 1.3em}",
            ".scene{text-align:center;color:#888;letter-spacing:0.3em;margin:1.5rem 0}</style></head><body>"]
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r'^#\s+', s):
            html.append(f"<h1>{re.sub(r'^#\\s+','',s)}</h1>")
        elif re.match(r'^##\s+', s):
            html.append(f"<h2>{re.sub(r'^##\\s+','',s)}</h2>")
        elif s == "***":
            html.append('<div class="scene">* * *</div>')
        else:
            html.append(f"<p>{s}</p>")
    html.append("</body></html>")
    return "\n".join(html)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_write, tab_audit, tab_find, tab_format, tab_preview, tab_export = st.tabs([
    "✍️ Write", "🔍 Audit", "🔎 Find", "🔧 Format", "📖 Preview", "⬇️ Export"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — WRITE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_write:
    st.markdown('<div class="slabel">Manuscript</div>', unsafe_allow_html=True)

    new_ms = st.text_area(
        "ms",
        value=st.session_state.manuscript,
        placeholder="Start writing or paste your manuscript here...\n\nTip: ## Chapter 1: Title for chapters · *** for scene breaks · # My Book Title for the title",
        height=400,
        label_visibility="collapsed",
    )
    if new_ms != st.session_state.manuscript:
        push_history(st.session_state.manuscript)
        st.session_state.manuscript = new_ms

    ms = st.session_state.manuscript
    if ms.strip():
        wc  = word_count(ms)
        sc  = sentence_count(ms)
        pc  = paragraph_count(ms)
        chs = len(detect_chapters(ms))
        pages = max(1, round(wc / 250))
        rt = max(1, round(wc / 238))

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.metric("Words", f"{wc:,}")
        with c2: st.metric("Pages ~", pages)
        with c3: st.metric("Sentences", sc)
        with c4: st.metric("Chapters", chs if chs else "—")
        with c5: st.metric("Read Time", f"{rt}m")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("↩️ Undo", use_container_width=True):
                if st.session_state.history:
                    st.session_state.manuscript = st.session_state.history.pop()
                    st.rerun()
                else:
                    st.info("Nothing to undo.")
        with col_b:
            if st.button("🗑️ Clear All", use_container_width=True):
                push_history(st.session_state.manuscript)
                st.session_state.manuscript = ""
                st.rerun()
    else:
        st.markdown("""
        <div class="card" style="margin-top:10px">
          <div class="card-title">Getting Started</div>
          <div class="card-body">
            Write directly or paste your full manuscript above.<br><br>
            <b>Book title:</b>&nbsp; <code># My Book Title</code><br>
            <b>Chapter:</b>&nbsp; <code>## Chapter 1: The Beginning</code><br>
            <b>Scene break:</b>&nbsp; <code>***</code> on its own line
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="slabel">Private Notes (never exported)</div>', unsafe_allow_html=True)
    notes = st.text_area("notes", value=st.session_state.notes,
                         placeholder="Plot notes, character outlines, reminders...",
                         height=110, label_visibility="collapsed")
    if notes != st.session_state.notes:
        st.session_state.notes = notes

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AUDIT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_audit:
    ms = st.session_state.manuscript
    if not ms.strip():
        st.markdown('<div class="issue-row info">ℹ Paste your manuscript in the Write tab first.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="slabel">Formatting Issues</div>', unsafe_allow_html=True)
        for issue in audit_text(ms):
            lvl = issue["level"]
            icon = {"ok": "✓", "warn": "⚠", "info": "ℹ", "err": "✗"}.get(lvl, "•")
            st.markdown(f'<div class="issue-row {lvl}">{icon} {issue["msg"]}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="slabel">Table of Contents</div>', unsafe_allow_html=True)
        toc = build_toc(ms)
        if toc:
            for e in toc:
                st.markdown(f"""
                <div class="toc-entry">
                  <span class="toc-title">{e['title']}</span>
                  <span class="toc-page">p. {e['page']}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="issue-row info">ℹ No headings found — add <code>## Chapter 1: Title</code> to build a TOC.</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="slabel">Word Frequency (top 15, excluding common words)</div>', unsafe_allow_html=True)
        stopwords = {"the","and","a","to","of","in","is","it","that","was","he","she","his","her",
                     "i","you","we","they","with","for","on","at","be","as","had","have","this",
                     "but","from","or","an","by","are","said","not","so","what","all","were","when",
                     "there","been","one","do","their","my","me","no","if","can","up","its","out",
                     "into","about","more","how","your","our","them","will","has","would","could",
                     "than","then","just","like","some","these","those","which","who","him","us"}
        freq = {}
        for w in re.findall(r'\b\w+\b', ms.lower()):
            if len(w) > 3 and w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:15]
        if top:
            mx = top[0][1]
            for word, count in top:
                bar = int((count / mx) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">
                  <span style="min-width:90px;font-size:0.8rem;color:#ccc">{word}</span>
                  <div style="flex:1;background:#1e1e20;border-radius:3px;height:7px">
                    <div style="width:{bar}%;background:#c9a84c;border-radius:3px;height:7px"></div>
                  </div>
                  <span style="font-size:0.74rem;color:#666;min-width:26px;text-align:right">{count}</span>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FIND & REPLACE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_find:
    ms = st.session_state.manuscript
    st.markdown('<div class="slabel">Find & Replace</div>', unsafe_allow_html=True)

    if not ms.strip():
        st.markdown('<div class="issue-row info">ℹ Paste your manuscript in the Write tab first.</div>', unsafe_allow_html=True)
    else:
        find_str    = st.text_input("Find",    placeholder='e.g. "said" or "John"',       key="find_in")
        replace_str = st.text_input("Replace with", placeholder='e.g. "whispered" or "James"', key="repl_in")

        col1, col2 = st.columns(2)
        with col1:
            case_sensitive = st.checkbox("Case sensitive", value=False, key="case_cb")
        with col2:
            whole_word = st.checkbox("Whole word only", value=False, key="whole_cb")

        if find_str:
            flags = 0 if case_sensitive else re.IGNORECASE
            pattern = (r'\b' + re.escape(find_str) + r'\b') if whole_word else re.escape(find_str)
            try:
                n = len(re.findall(pattern, ms, flags=flags))
                st.markdown(f'<div class="match-count">🔍 {n} match(es) found</div>', unsafe_allow_html=True)
            except re.error:
                pass

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Replace All", use_container_width=True, key="rep_btn"):
                if find_str:
                    push_history(ms)
                    new_ms, n = find_replace(ms, find_str, replace_str, case_sensitive, whole_word)
                    st.session_state.manuscript = new_ms
                    st.success(f"Replaced {n} occurrence(s).")
                    st.rerun()
        with col_b:
            if st.button("↩️ Undo", use_container_width=True, key="fr_undo"):
                if st.session_state.history:
                    st.session_state.manuscript = st.session_state.history.pop()
                    st.success("Undone.")
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — FORMAT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_format:
    ms = st.session_state.manuscript
    st.markdown('<div class="slabel">Auto-Format Options</div>', unsafe_allow_html=True)

    if not ms.strip():
        st.markdown('<div class="issue-row info">ℹ Paste your manuscript in the Write tab first.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card"><div class="card-body">Select fixes to apply, then tap <b>Apply Formatting</b>. All changes are undoable.</div></div>', unsafe_allow_html=True)

        opts = {}
        opts["double_space"]     = st.checkbox("Remove double spaces",                             value=True)
        opts["blank_lines"]      = st.checkbox("Collapse 3+ blank lines → single blank line",      value=True)
        opts["strip_trailing"]   = st.checkbox("Strip trailing whitespace from lines",              value=True)
        opts["smart_quotes"]     = st.checkbox('Convert straight "quotes" → "smart quotes"',       value=False)
        opts["ellipsis"]         = st.checkbox("Convert ... → … (ellipsis character)",             value=False)
        opts["em_dash"]          = st.checkbox("Convert -- or --- → — (em dash)",                  value=False)
        opts["scene_break"]      = st.checkbox("Normalize * * * / --- scene breaks → ***",         value=False)
        opts["chapter_headings"] = st.checkbox("Normalize bare 'Chapter N' lines → ## Chapter N", value=False)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Apply Formatting", use_container_width=True):
                push_history(ms)
                st.session_state.manuscript = auto_format(ms, opts)
                st.success("Formatting applied!")
                st.rerun()
        with col_b:
            if st.button("↩️ Undo", use_container_width=True, key="fmt_undo"):
                if st.session_state.history:
                    st.session_state.manuscript = st.session_state.history.pop()
                    st.success("Undone.")
                    st.rerun()
                else:
                    st.info("Nothing to undo.")

        st.markdown("---")
        st.markdown('<div class="slabel">Print / KDP Reference Specs</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <div class="card-title">Standard KDP Print-on-Demand Specs</div>
          <div class="card-body">
            <b>Trim sizes:</b> 5×8″ (novels) · 6×9″ (nonfiction) · 5.5×8.5″ (general fiction)<br>
            <b>Margins:</b> Inside 0.875″ · Outside 0.625″ · Top/Bottom 0.75″<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(add 0.125″ inside for 250+ pages)<br>
            <b>Body font:</b> Garamond 11–12pt · Times New Roman 11pt<br>
            <b>Line spacing:</b> 1.2–1.4× for novels · 1.3–1.5× for nonfiction<br>
            <b>Indent:</b> 0.25–0.3″ (no indent on first para after heading)<br>
            <b>Scene breaks:</b> Centered *** · blank line above and below<br>
            <b>Chapter open:</b> Start ~⅓ down page · drop cap or small caps on first word<br>
            <b>Page numbers:</b> Footer · no number on chapter-opening pages<br>
            <b>Widows/Orphans:</b> Minimum 2 lines at top/bottom of any page
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PREVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab_preview:
    ms = st.session_state.manuscript
    st.markdown('<div class="slabel">Book Page Preview</div>', unsafe_allow_html=True)

    if not ms.strip():
        st.markdown('<div class="issue-row info">ℹ Write something first to see the preview.</div>', unsafe_allow_html=True)
    else:
        parts = []
        for line in ms.split("\n"):
            s = line.strip()
            if not s:
                parts.append('<div style="height:0.85rem"></div>')
            elif re.match(r'^#\s+', s):
                t = re.sub(r'^#\s+', '', s)
                parts.append(f'<h1 style="font-size:1.5rem;text-align:center;margin:1.5rem 0 1rem;font-family:Playfair Display,serif;color:#111">{t}</h1>')
            elif re.match(r'^##\s+', s):
                t = re.sub(r'^##\s+', '', s)
                parts.append(f'<h2 style="font-size:1.05rem;margin:2rem 0 0.3rem;font-family:Playfair Display,serif;color:#222;border-bottom:1px solid #ccc;padding-bottom:4px">{t}</h2>')
            elif s == "***":
                parts.append('<div style="text-align:center;margin:1.2rem 0;color:#999;letter-spacing:0.35em">* * *</div>')
            else:
                parts.append(f'<p style="margin:0 0 0 1.3em;text-indent:0;color:#1a1a1a">{s}</p>')

        st.markdown(f'<div class="page-preview">{"".join(parts)}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_export:
    ms = st.session_state.manuscript
    st.markdown('<div class="slabel">Export</div>', unsafe_allow_html=True)

    if not ms.strip():
        st.markdown('<div class="issue-row info">ℹ Nothing to export yet.</div>', unsafe_allow_html=True)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        wc = word_count(ms)
        st.markdown(f'<div class="card"><div class="card-title">Ready to Export</div><div class="card-body">{wc:,} words · ~{max(1,round(wc/250))} pages</div></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("⬇️ .txt", data=ms,
                               file_name=f"manuscript_{ts}.txt", mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("⬇️ .md", data=ms,
                               file_name=f"manuscript_{ts}.md", mime="text/markdown", use_container_width=True)
        with c3:
            st.download_button("⬇️ .html", data=export_html(ms),
                               file_name=f"manuscript_{ts}.html", mime="text/html", use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="slabel">Publishing Checklist</div>', unsafe_allow_html=True)

        checklist = [
            ("Ebook", [
                "Chapter headings use ## format (needed for NCX/TOC in ebook readers)",
                "No manual page breaks — ebook formatters handle reflow",
                "Scene breaks use *** (not ---)",
                "Smart quotes used throughout",
                "No double spaces or tab-based paragraph indents",
                "Front matter present: title page, copyright page, dedication",
                "Back matter present: About the Author, newsletter / CTA page",
                "Paste .txt or .md into Atticus, Reedsy, or Kindle Create",
            ]),
            ("Print PDF", [
                "Correct trim size set before flowing text",
                "Inside margin ≥ 0.875″ (add 0.125″ for books over 150 pages)",
                "All fonts embedded before PDF export",
                "Chapter-opening pages start approximately ⅓ down the page",
                "No page number on chapter-opening pages",
                "Widows and orphans fixed manually before final export",
                "Image resolution ≥ 300 DPI if images are present",
                "Export as PDF/X-1a for KDP compatibility",
            ]),
            ("Retailer Upload", [
                "Cover: 2,560 × 1,600 px minimum (JPG/TIFF, separate from manuscript)",
                "Separate ISBNs for ebook and print editions",
                "BISAC category selected (2–3 maximum)",
                "7 keywords entered — use phrases, not single words",
                "Book description previewed in KDP (HTML tags supported)",
                "Author Central page claimed and linked to book",
            ]),
        ]

        for section, items in checklist:
            st.markdown(f"<div class='slabel' style='margin-top:16px'>{section}</div>", unsafe_allow_html=True)
            for item in items:
                st.markdown(f"""
                <div style="display:flex;gap:10px;align-items:flex-start;padding:6px 0;
                     border-bottom:1px solid #1a1a1c;font-size:0.8rem;color:#bbb">
                  <span style="color:#c9a84c;flex-shrink:0;margin-top:1px">◇</span>
                  <span>{item}</span>
                </div>""", unsafe_allow_html=True)
