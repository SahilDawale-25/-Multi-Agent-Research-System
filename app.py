import streamlit as st
import time
from pipeline import run_research_pipeline

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #050508 !important;
    color: #e8e4f0 !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(108,43,217,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(20,184,166,0.12) 0%, transparent 55%),
        #050508 !important;
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* ── Hero Header ── */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; font-weight: 500; letter-spacing: 0.18em;
    color: #a78bfa;
    background: rgba(109,40,217,0.12);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 999px; padding: 5px 14px; margin-bottom: 1.4rem;
}
.hero-dot { width: 6px; height: 6px; border-radius: 50%; background: #a78bfa;
            animation: pulse-dot 1.8s ease-in-out infinite; }
@keyframes pulse-dot {
    0%,100% { opacity:1; transform: scale(1); }
    50%      { opacity:0.4; transform: scale(0.7); }
}
.hero-title {
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    font-weight: 800; line-height: 1.05; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 0%, #c4b5fd 45%, #5eead4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 0.8rem;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    color: rgba(200,190,220,0.55); font-size: 0.9rem; letter-spacing: 0.05em;
}

/* ── Input Area ── */
.input-shell {
    background: rgba(255,255,255,0.028);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 18px; padding: 2rem 2.2rem; margin: 2rem 0;
    backdrop-filter: blur(12px);
    transition: border-color 0.3s;
}
.input-shell:hover { border-color: rgba(139,92,246,0.45); }
.input-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; color: #7c3aed; text-transform: uppercase;
    margin-bottom: 0.8rem;
}

[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 12px !important;
    color: #ede9fe !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.9rem 1.2rem !important;
    transition: all 0.25s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(139,92,246,0.7) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
    background: rgba(255,255,255,0.06) !important;
}
[data-testid="stTextInput"] input::placeholder { color: rgba(167,139,250,0.35) !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100%; padding: 0.9rem 2rem !important;
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important; border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 1rem !important; letter-spacing: 0.04em !important;
    cursor: pointer !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.35) !important;
    transition: all 0.25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.5) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Pipeline Steps ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(255,255,255,0.05);
    border-radius: 16px; overflow: hidden;
    margin: 2rem 0; border: 1px solid rgba(255,255,255,0.06);
}
.pipeline-step {
    background: rgba(255,255,255,0.025);
    padding: 1.4rem 1.2rem;
    position: relative; text-align: center;
    transition: background 0.3s;
}
.pipeline-step.active  { background: rgba(124,58,237,0.15); }
.pipeline-step.done    { background: rgba(20,184,166,0.1); }
.pipeline-step.waiting { opacity: 0.45; }

.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.18em;
    color: rgba(167,139,250,0.5); margin-bottom: 0.5rem;
}
.step-icon { font-size: 1.6rem; margin-bottom: 0.5rem; display: block; }
.step-name {
    font-weight: 700; font-size: 0.82rem; color: #ddd6fe;
    margin-bottom: 0.25rem;
}
.step-desc {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; color: rgba(200,190,220,0.4);
    line-height: 1.5;
}
.step-bar {
    height: 2px; border-radius: 2px; margin-top: 1rem;
    background: rgba(255,255,255,0.06);
    overflow: hidden;
}
.step-fill {
    height: 100%; border-radius: 2px;
    background: linear-gradient(90deg, #7c3aed, #5eead4);
}
.step-fill.active  { width: 60%; animation: bar-anim 1.2s ease-in-out infinite alternate; }
.step-fill.done    { width: 100%; background: linear-gradient(90deg,#14b8a6,#06b6d4); }
.step-fill.waiting { width: 0%; }
@keyframes bar-anim {
    from { width: 30%; opacity: 0.7; }
    to   { width: 90%; opacity: 1; }
}

/* ── Result Cards ── */
.result-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 1.4rem;
    position: relative; overflow: hidden;
    transition: border-color 0.3s, transform 0.2s;
}
.result-card:hover { border-color: rgba(139,92,246,0.3); transform: translateY(-1px); }
.result-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
}
.card-search::before  { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.card-reader::before  { background: linear-gradient(90deg, #0891b2, #22d3ee); }
.card-report::before  { background: linear-gradient(90deg, #059669, #34d399); }
.card-critic::before  { background: linear-gradient(90deg, #d97706, #fbbf24); }

.card-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1.2rem;
}
.card-icon { font-size: 1.3rem; }
.card-title {
    font-weight: 700; font-size: 1rem; color: #ede9fe;
    letter-spacing: 0.01em;
}
.card-tag {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.15em;
    padding: 3px 10px; border-radius: 999px;
    text-transform: uppercase;
}
.card-search .card-tag  { background: rgba(124,58,237,0.2); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
.card-reader .card-tag  { background: rgba(8,145,178,0.2); color: #22d3ee; border: 1px solid rgba(8,145,178,0.3); }
.card-report .card-tag  { background: rgba(5,150,105,0.2); color: #34d399; border: 1px solid rgba(5,150,105,0.3); }
.card-critic .card-tag  { background: rgba(217,119,6,0.2);  color: #fbbf24; border: 1px solid rgba(217,119,6,0.3); }

.card-content {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem; line-height: 1.75; color: rgba(220,210,240,0.75);
    white-space: pre-wrap; word-break: break-word;
    max-height: 320px; overflow-y: auto;
    padding-right: 4px;
}
.card-content::-webkit-scrollbar { width: 4px; }
.card-content::-webkit-scrollbar-track { background: transparent; }
.card-content::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 2px; }

/* ── Status Toast ── */
.status-toast {
    display: flex; align-items: center; gap: 12px;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 12px; padding: 1rem 1.4rem; margin: 1rem 0;
}
.toast-spinner {
    width: 18px; height: 18px; border-radius: 50%;
    border: 2px solid rgba(167,139,250,0.25);
    border-top-color: #a78bfa;
    animation: spin 0.8s linear infinite; flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
.toast-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; color: #c4b5fd; letter-spacing: 0.05em;
}

/* ── Divider ── */
.fancy-div {
    display: flex; align-items: center; gap: 12px; margin: 2rem 0;
    color: rgba(200,190,220,0.2); font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.15em;
}
.fancy-div::before, .fancy-div::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.2), transparent);
}

/* ── Success Banner ── */
.success-banner {
    text-align: center; padding: 1.2rem;
    background: rgba(20,184,166,0.08);
    border: 1px solid rgba(20,184,166,0.2);
    border-radius: 14px; margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; color: #5eead4; letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">
        <div class="hero-dot"></div>
        MULTI-AGENT · AI RESEARCH SYSTEM
    </div>
    <div class="hero-title">ResearchMind</div>
    <div class="hero-sub">search → scrape → write → critique · powered by LangChain agents</div>
</div>
""", unsafe_allow_html=True)


# ─── Pipeline Visual (static intro) ──────────────────────────────────────────
def render_pipeline(statuses: dict):
    """statuses: {1:'waiting'|'active'|'done', 2:..., 3:..., 4:...}"""
    steps = [
        (1, "🔍", "Search Agent",   "Web search &\nsource discovery"),
        (2, "📄", "Reader Agent",   "Scrape &\nextract content"),
        (3, "✍️", "Writer Chain",   "Draft structured\nresearch report"),
        (4, "🎯", "Critic Chain",   "Review &\nfeedback loop"),
    ]
    html = '<div class="pipeline-grid">'
    for num, icon, name, desc in steps:
        s = statuses.get(num, 'waiting')
        html += f"""
        <div class="pipeline-step {s}">
            <div class="step-num">STEP {num:02d}</div>
            <span class="step-icon">{icon}</span>
            <div class="step-name">{name}</div>
            <div class="step-desc">{desc}</div>
            <div class="step-bar"><div class="step-fill {s}"></div></div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


render_pipeline({1:'waiting',2:'waiting',3:'waiting',4:'waiting'})


# ─── Input ───────────────────────────────────────────────────────────────────
st.markdown('<div class="input-shell">', unsafe_allow_html=True)
st.markdown('<div class="input-label">⬡ Research Topic</div>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        label="topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025…",
        label_visibility="collapsed",
        key="topic_input",
    )
with col2:
    run_btn = st.button("⚡ Run Pipeline", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─── Run Pipeline ────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown("""
        <div class="status-toast">
            <div style="font-size:1.2rem">⚠️</div>
            <div class="toast-text">Please enter a research topic before running the pipeline.</div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="fancy-div">PIPELINE EXECUTION</div>', unsafe_allow_html=True)

    # ── Step placeholders
    pipeline_ph = st.empty()
    toast_ph    = st.empty()

    def show_status(statuses, msg):
        with pipeline_ph.container():
            render_pipeline(statuses)
        toast_ph.markdown(f"""
        <div class="status-toast">
            <div class="toast-spinner"></div>
            <div class="toast-text">{msg}</div>
        </div>""", unsafe_allow_html=True)

    # ── Step 1
    show_status({1:'active',2:'waiting',3:'waiting',4:'waiting'},
                "Step 01 · Search Agent — scouring the web for sources…")

    from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
    import streamlit as _st

    state = {}

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    # ── Step 2
    show_status({1:'done',2:'active',3:'waiting',4:'waiting'},
                "Step 02 · Reader Agent — scraping top resources for deep content…")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search result about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}")]
    })
    state["scraped_content"] = reader_result['messages'][-1].content

    # ── Step 3
    show_status({1:'done',2:'done',3:'active',4:'waiting'},
                "Step 03 · Writer Chain — drafting the research report…")

    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    # ── Step 4
    show_status({1:'done',2:'done',3:'done',4:'active'},
                "Step 04 · Critic Chain — reviewing and providing feedback…")

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    # Done!
    show_status({1:'done',2:'done',3:'done',4:'done'}, "")
    toast_ph.empty()

    # ── Success Banner
    st.markdown(f"""
    <div class="success-banner">
        ✦ Pipeline complete · Topic: <strong>{topic}</strong> · All 4 agents executed successfully
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="fancy-div">RESULTS</div>', unsafe_allow_html=True)

    # ── Result Cards
    cards = [
        ("card-search", "🔍", "Search Results",    "SEARCH",  state["search_results"]),
        ("card-reader", "📄", "Scraped Content",   "READER",  state["scraped_content"]),
        ("card-report", "✍️", "Research Report",   "WRITER",  state["report"]),
        ("card-critic", "🎯", "Critic Feedback",   "CRITIC",  state["feedback"]),
    ]
    for cls, icon, title, tag, content in cards:
        text = content if isinstance(content, str) else str(content)
        st.markdown(f"""
        <div class="result-card {cls}">
            <div class="card-header">
                <span class="card-icon">{icon}</span>
                <span class="card-title">{title}</span>
                <span class="card-tag">{tag}</span>
            </div>
            <div class="card-content">{text}</div>
        </div>""", unsafe_allow_html=True)
