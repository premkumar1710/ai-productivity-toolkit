"""
AI Productivity Toolkit - Modern Streamlit Web UI
Interactive dashboard for Summarization, Email, Resume Optimization, and Coding/Research.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import json
from day_10_productivity_toolkit.config import ToolkitConfig
from day_10_productivity_toolkit.llm_client import LLMClient
from day_10_productivity_toolkit.modules.summarizer import SummarizerWorkflow
from day_10_productivity_toolkit.modules.email_assistant import EmailAssistantWorkflow
from day_10_productivity_toolkit.modules.resume_optimizer import ResumeOptimizerWorkflow
from day_10_productivity_toolkit.modules.coding_assistant import CodingAssistantWorkflow

st.set_page_config(
    page_title="AI Productivity Toolkit",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E88E5; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #546E7A; margin-bottom: 1.5rem; }
    .card { background-color: #F8F9FA; border-radius: 8px; padding: 1.2rem; border-left: 4px solid #1E88E5; }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚡ AI Toolkit Settings")
cfg = ToolkitConfig.load()
st.sidebar.info(f"**Backend Provider:** {cfg.provider.upper()}\n\n**Model:** `{cfg.model_name}`")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Modules
- 📝 **Executive Summarizer**
- ✉️ **Smart Email Assistant**
- 📄 **Resume & Career Optimizer**
- 💻 **Coding & Research Lab**
""")

client = LLMClient(cfg)

# Header
st.markdown('<div class="main-title">AI Productivity Toolkit</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">High-performance reusable prompt engineering workflows for daily engineering productivity.</div>', unsafe_allow_html=True)

tabs = st.tabs([
    "📝 Summarizer",
    "✉️ Email Assistant",
    "📄 Resume Optimizer",
    "💻 Coding & Research",
    "📊 System Architecture"
])

# ----------------- TAB 1: SUMMARIZER -----------------
with tabs[0]:
    st.subheader("Executive Text Summarizer")
    col1, col2 = st.columns([1, 1])

    with col1:
        default_doc = (
            "During Q3, engineering achieved 99.98% platform uptime, exceeding the 99.95% SLA. "
            "P99 latency decreased from 450ms to 230ms after implementing Redis clustering. "
            "Monthly cloud database costs fell by $14,000. For next sprint, Bob must finalize "
            "the multi-region failover and Sarah will lead the security penetration audit."
        )
        doc_input = st.text_area("Source Document / Meeting Notes / Article", value=default_doc, height=200)
        fmt = st.selectbox("Format", ["Executive Brief", "TL;DR", "Action Items Only", "Full Digest"])
        audience = st.selectbox("Audience", ["Leadership & Stakeholders", "Engineering Team", "General Public"])
        word_limit = st.slider("Word Limit", 50, 500, 200, step=25)
        run_sum = st.button("Generate Summary", type="primary", key="btn_sum")

    with col2:
        if run_sum or doc_input:
            wf = SummarizerWorkflow(client)
            result = wf.summarize(doc_input, format_type=fmt, audience=audience, max_words=word_limit)
            st.markdown("### Output")
            st.markdown(result["summary"])
            st.caption(f"Estimated Word Count: {result['word_count']} words")

# ----------------- TAB 2: EMAIL ASSISTANT -----------------
with tabs[1]:
    st.subheader("Smart Email Assistant")
    col1, col2 = st.columns([1, 1])

    with col1:
        default_email = "Can you send over the updated project timeline and confirm if we're on track for Friday's release?"
        email_ctx = st.text_area("Incoming Email or Purpose", value=default_email, height=160)
        mode = st.selectbox("Email Mode", ["Reply to Email", "Cold Outreach", "Follow-up", "Meeting Scheduling"])
        tone = st.selectbox("Tone", ["Executive & Crisp", "Warm & Collaborative", "Direct & Assertive", "Polite De-escalation"])
        sender = st.text_input("Your Name / Signature", value="Alex Morgan")
        recipient = st.text_input("Recipient", value="Engineering Team")
        run_email = st.button("Generate Draft", type="primary", key="btn_email")

    with col2:
        if run_email or email_ctx:
            wf = EmailAssistantWorkflow(client)
            draft = wf.generate_email(email_ctx, mode=mode, tone=tone, sender_name=sender, recipient_name=recipient)
            st.text_input("Generated Subject", value=draft["subject"])
            st.text_area("Draft Body", value=draft["body"], height=220)

# ----------------- TAB 3: RESUME OPTIMIZER -----------------
with tabs[2]:
    st.subheader("Resume & ATS Career Optimizer")
    col1, col2 = st.columns([1, 1])

    with col1:
        default_resume = "Software Engineer with 4 years building backend APIs in Python and working with PostgreSQL databases."
        default_jd = "Senior Python Engineer required. Must have experience scaling microservices, Redis caching, Kubernetes, and high availability systems."
        resume_in = st.text_area("Candidate Resume Experience", value=default_resume, height=150)
        jd_in = st.text_area("Target Job Description", value=default_jd, height=150)
        run_resume = st.button("Run ATS Gap Analysis", type="primary", key="btn_resume")

    with col2:
        if run_resume or resume_in:
            wf = ResumeOptimizerWorkflow(client)
            res = wf.optimize(resume_in, jd_in)
            
            st.metric("ATS Match Score", f"{res.match_score} / 100")
            
            st.markdown("#### Top Strengths")
            for s in res.strengths:
                st.markdown(f"✅ {s}")
                
            st.markdown("#### Skills Gap")
            for g in res.skills_gap:
                st.markdown(f"⚠️ {g}")

            st.markdown("#### Enhanced Bullet Points (Google XYZ Formula)")
            for b in res.enhanced_bullet_points:
                st.info(f"💡 {b}")

# ----------------- TAB 4: CODING & RESEARCH -----------------
with tabs[3]:
    st.subheader("Coding & Research Assistant")
    col1, col2 = st.columns([1, 1])

    with col1:
        default_code = """def find_duplicates(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates"""
        code_in = st.text_area("Code Snippet or Architecture Query", value=default_code, height=200)
        task_choice = st.selectbox("Task", ["Explain Code", "Generate Unit Tests", "Debug & Refactor", "Research Summarization"])
        lang = st.selectbox("Language", ["python", "typescript", "golang", "sql"])
        run_code = st.button("Execute Task", type="primary", key="btn_code")

    with col2:
        if run_code or code_in:
            wf = CodingAssistantWorkflow(client)
            res = wf.process_code_task(code_in, task=task_choice, language=lang)
            st.markdown(res["result"])

# ----------------- TAB 5: ARCHITECTURE -----------------
with tabs[4]:
    st.subheader("Architecture & Design")
    st.markdown("""
    The **AI Productivity Toolkit** is organized around production prompt engineering principles:
    - **Scaffolding:** Strict persona, context, delimiters, and negative constraints.
    - **Structured Validation:** Pydantic schema parsing with resilient JSON extraction and repair.
    - **Multi-Provider Support:** Supports Google Gemini, OpenAI, Anthropic, and deterministic Offline Mocking.
    - **Evaluation Harness:** Reusable Jinja-style prompt templates, regression testing, and automated benchmark scoring.
    """)
