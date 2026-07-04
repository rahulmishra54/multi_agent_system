import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #09090B;
    --card: #18181B;
    --accent: #7C3AED;
    --accent2: #3B82F6;
    --text: #FAFAFA;
    --muted: #A1A1AA;
    --success: #22C55E;
    --border: rgba(255,255,255,0.08);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 70% 45% at 15% -10%, rgba(124,58,237,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 85% 0%, rgba(59,130,246,0.10) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 3rem 4rem; max-width: 1180px; }

/* ── Fade-in ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeInUp 0.5s ease both; }

/* ── Top nav ── */
.topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.4rem;
    background: rgba(24,24,27,0.6);
    border: 1px solid var(--border);
    border-radius: 14px;
    backdrop-filter: blur(14px);
    margin-bottom: 2rem;
}
.topnav-left { display: flex; align-items: center; gap: 0.7rem; }
.topnav-logo {
    width: 34px; height: 34px;
    border-radius: 9px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    box-shadow: 0 4px 16px rgba(124,58,237,0.35);
}
.topnav-name {
    font-weight: 700;
    font-size: 1.02rem;
    letter-spacing: -0.01em;
    color: var(--text);
}
.topnav-right { display: flex; align-items: center; gap: 0.6rem; }
.model-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    color: var(--accent2);
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.25);
    padding: 0.32rem 0.7rem;
    border-radius: 999px;
}
.settings-icon {
    width: 30px; height: 30px;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
    color: var(--muted);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0c0c0f;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding: 1.4rem 1rem; }
.sidebar-section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.3rem 0 0.6rem 0.2rem;
}
.sidebar-item {
    padding: 0.55rem 0.75rem;
    border-radius: 9px;
    font-size: 0.85rem;
    color: var(--muted);
    background: transparent;
    border: 1px solid transparent;
    margin-bottom: 0.35rem;
    transition: all 0.15s;
}
.sidebar-item:hover {
    background: rgba(255,255,255,0.04);
    border-color: var(--border);
    color: var(--text);
}
.sidebar-empty {
    font-size: 0.78rem;
    color: #52525b;
    padding: 0.4rem 0.75rem;
    font-style: italic;
}

section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--accent), #6d28d9) !important;
    color: #fff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    width: 100%;
    box-shadow: 0 4px 14px rgba(124,58,237,0.3) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 1.5rem 0 2.2rem;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: 1rem;
    opacity: 0.95;
}
.hero h1 {
    font-family: 'Inter', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 400;
    color: var(--muted);
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Input card (glassmorphism) ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--accent2) !important;
    font-weight: 500 !important;
}

/* ── Button (gradient) ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 6px 22px rgba(124,58,237,0.35) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(124,58,237,0.45) !important;
    opacity: 0.97 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Example chips ── */
.chip-row { display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1.8rem; align-items:center; }
.chip-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    color: #52525b;
    letter-spacing: 0.12em;
}
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.32rem 0.85rem;
    font-size: 0.78rem;
    color: var(--muted);
    transition: all 0.15s;
}
.chip:hover {
    border-color: rgba(124,58,237,0.4);
    color: var(--text);
    background: rgba(124,58,237,0.08);
}

/* ── Pipeline step cards ── */
.step-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: rgba(255,255,255,0.06);
    transition: background 0.3s;
}
.step-card.active {
    border-color: rgba(124,58,237,0.45);
    background: linear-gradient(135deg, rgba(124,58,237,0.07), rgba(24,24,27,1));
    box-shadow: 0 8px 26px rgba(124,58,237,0.15);
}
.step-card.active::before {
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}
.step-card.done {
    border-color: rgba(34,197,94,0.3);
    background: rgba(34,197,94,0.04);
}
.step-card.done::before { background: var(--success); }

.step-header { display: flex; align-items: center; gap: 0.8rem; }
.step-icon {
    width: 34px; height: 34px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    background: rgba(255,255,255,0.05);
    flex-shrink: 0;
}
.step-card.active .step-icon { background: rgba(124,58,237,0.18); }
.step-card.done .step-icon { background: rgba(34,197,94,0.15); }
.step-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text);
}
.step-desc { font-size: 0.76rem; color: var(--muted); margin-top: 0.15rem; }
.step-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    white-space: nowrap;
}
.status-waiting { color: #52525b; background: rgba(255,255,255,0.03); }
.status-running {
    color: var(--accent);
    background: rgba(124,58,237,0.12);
    animation: pulse 1.4s ease-in-out infinite;
}
.status-done { color: var(--success); background: rgba(34,197,94,0.12); }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.55; } }

/* ── Progress bar shimmer for active card ── */
.progress-track {
    height: 3px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    margin-top: 0.9rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    width: 40%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 2px;
    animation: slide 1.2s ease-in-out infinite;
}
@keyframes slide {
    0% { margin-left: -40%; }
    100% { margin-left: 100%; }
}

/* ── Section heading ── */
.section-heading {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    margin: 1.6rem 0 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.section-heading .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
}

/* ── Result / report / feedback panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem 1.7rem;
    margin-top: 0.4rem;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.result-content {
    font-size: 0.88rem;
    line-height: 1.75;
    color: #d4d4d8;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

.report-panel, .feedback-panel {
    background: var(--card);
    border-radius: 18px;
    padding: 2rem 2.3rem;
    margin-top: 0.8rem;
    box-shadow: 0 10px 36px rgba(0,0,0,0.3);
}
.report-panel { border: 1px solid rgba(124,58,237,0.25); }
.feedback-panel { border: 1px solid rgba(34,197,94,0.22); }

.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.panel-label.purple { color: var(--accent); border-bottom: 1px solid rgba(124,58,237,0.2); }
.panel-label.green  { color: var(--success); border-bottom: 1px solid rgba(34,197,94,0.2); }

.report-panel .stMarkdown, .feedback-panel .stMarkdown { color: #e4e4e7; }
.report-panel table, .feedback-panel table { border-color: var(--border) !important; }

/* ── Spinner ── */
.stSpinner > div { color: var(--accent) !important; }

/* ── Expander / accordion ── */
.streamlit-expanderHeader, details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.76rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.08em !important;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.3rem !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(124,58,237,0.08) !important;
}

/* ── Copy button (custom html) ── */
.copy-btn-wrap { display: flex; justify-content: flex-end; margin-top: -0.5rem; margin-bottom: 0.6rem; }

/* ── Footer notice ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #3f3f46;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    icon_map = {"01": "🔍", "02": "📄", "03": "✍️", "04": "🧐"}
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    progress_html = '<div class="progress-track"><div class="progress-fill"></div></div>' if state == "running" else ""
    st.markdown(f"""
    <div class="step-card {card_cls} fade-in">
        <div class="step-header">
            <div class="step-icon">{icon_map.get(num, "●")}</div>
            <div>
                <div class="step-title">{title}</div>
                {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
            </div>
            <span class="step-status {cls}">{label}</span>
        </div>
        {progress_html}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Top navigation ────────────────────────────────────────────────────────────
st.markdown("""
<div class="topnav fade-in">
    <div class="topnav-left">
        <div class="topnav-logo">🔬</div>
        <div class="topnav-name">ResearchMind</div>
    </div>
    <div class="topnav-right">
        <span class="model-badge">MULTI-AGENT · v1</span>
        <div class="settings-icon">⚙️</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="topnav-name" style="margin-bottom:0.8rem;">🔬 ResearchMind</div>', unsafe_allow_html=True)

    new_chat = st.button("＋  New Chat", use_container_width=True)
    if new_chat:
        st.session_state.results = {}
        st.session_state.running = False
        st.session_state.done = False
        st.rerun()

    st.markdown('<div class="sidebar-section-title">Chat History</div>', unsafe_allow_html=True)
    current_topic = st.session_state.get("topic_input", "")
    if current_topic and (st.session_state.results or st.session_state.running):
        st.markdown(f'<div class="sidebar-item">💬 {current_topic}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-empty">No conversations yet</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Saved Reports</div>', unsafe_allow_html=True)
    if st.session_state.done and st.session_state.results.get("writer"):
        st.markdown(f'<div class="sidebar-item">📄 {current_topic or "Untitled report"}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-empty">Reports appear here once generated</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Recent Topics</div>', unsafe_allow_html=True)
    if current_topic:
        st.markdown(f'<div class="sidebar-item">🕘 {current_topic}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-empty">Your topics will show up here</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Settings</div>', unsafe_allow_html=True)
    with st.expander("⚙️ Preferences"):
        st.caption("Model: Multi-Agent Pipeline v1")
        st.caption("Theme: Dark (default)")
        st.caption("Pipeline: Search → Read → Write → Critique")


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero fade-in">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card fade-in">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown('<div class="chip-row fade-in"><span class="chip-label">TRY →</span>', unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f'<span class="chip">{ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading"><span class="dot"></span>Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading"><span class="dot"></span>Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍  Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄  Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel fade-in">
            <div class="panel-label purple"><span>📝 Final Research Report</span></div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        dl_col, _ = st.columns([1, 3])
        with dl_col:
            st.download_button(
                label="⬇  Download Report (.md)",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
            )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel fade-in">
            <div class="panel-label green"><span>🧐 Critic Feedback</span></div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)