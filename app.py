"""Streamlit UI for the AI HR Recruitment Assistant -- White + Navy Blue
premium theme.

Run with:
    streamlit run app.py

All original functionality is unchanged: upload a resume + job description,
run the same src/pipeline.screen_candidate() flow (parse_resume ->
parse_job_description -> match_candidate_to_job -> generate_interview_questions),
and display the result. Only the visual layer is new.
"""
import os
import tempfile

import streamlit as st
import streamlit.components.v1 as components

from src.pipeline import screen_candidate
from src.ui.theme import BASE_CSS
from src.ui.report import build_report_html

st.set_page_config(page_title="AI HR Recruitment Assistant", page_icon="🧭", layout="wide")
st.markdown(BASE_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------- Top bar --
st.markdown(
    """
    <div class="hr-topbar">
      <div class="hr-topbar-inner">
        <div class="hr-logo">HR<span>AI</span></div>
        <div class="hr-topbar-badge">Agent&nbsp;+&nbsp;Tools&nbsp;+&nbsp;RAG</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------- Hero --
st.markdown(
    """
    <div class="hr-hero">
      <div class="hr-hero-badge">AI-Powered Recruiting</div>
      <h1 class="hr-hero-title">AI HR Recruitment <span>Assistant</span></h1>
      <p class="hr-hero-sub">
        Screen resumes, match candidates to job descriptions, and generate
        tailored interview questions &mdash; powered by an autonomous agent,
        purpose-built tools, and retrieval-augmented generation.
      </p>
      <div class="hr-chip-row">
        <div class="hr-chip">&#128196;&nbsp; Resume Screening</div>
        <div class="hr-chip">&#127919;&nbsp; Smart Matching</div>
        <div class="hr-chip">&#128172;&nbsp; Interview Prep</div>
        <div class="hr-chip">&#128218;&nbsp; RAG-Grounded</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------- Upload cards --
st.markdown('<div class="hr-section-label">Upload &amp; Screen</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="hr-card-label">&#128196; Candidate Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader(
        "Resume", type=["pdf", "docx", "txt"], label_visibility="collapsed", key="resume"
    )
with col2:
    st.markdown('<div class="hr-card-label">&#129534; Job Description</div>', unsafe_allow_html=True)
    jd_file = st.file_uploader(
        "Job description", type=["pdf", "docx", "txt"], label_visibility="collapsed", key="jd"
    )

screen_clicked = st.button(
    "Screen Candidate", type="primary", disabled=not (resume_file and jd_file)
)

if screen_clicked:
    with tempfile.TemporaryDirectory() as tmp:
        resume_path = os.path.join(tmp, resume_file.name)
        jd_path = os.path.join(tmp, jd_file.name)
        with open(resume_path, "wb") as f:
            f.write(resume_file.getbuffer())
        with open(jd_path, "wb") as f:
            f.write(jd_file.getbuffer())

        with st.spinner("Parsing resume & JD, matching, and generating interview questions..."):
            result = screen_candidate(resume_path, jd_path)

    st.session_state["hr_result"] = result

# ------------------------------------------------------------------- Report --
if "hr_result" in st.session_state:
    result = st.session_state["hr_result"]

    report_html = build_report_html(
        candidate=result["candidate"],
        jd=result["job_description"],
        match=result["match"],
        questions=result["interview_questions"],
    )
    components.html(report_html, height=1500, scrolling=True)

    with st.expander("Full extracted candidate profile (raw JSON)"):
        st.json(result["candidate"])
    with st.expander("Full parsed job description (raw JSON)"):
        st.json(result["job_description"])
else:
    st.markdown(
        '<div class="hr-empty-state">Upload a resume and a job description above, '
        "then click <strong>Screen Candidate</strong> to see the animated match report.</div>",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------- Footer --
st.markdown(
    """
    <div class="hr-footer">
      <div class="hr-footer-inner">
        <div class="hr-logo">HR<span>AI</span></div>
        <div class="hr-footer-links"><span>Agent</span><span>&middot;</span><span>Tools</span><span>&middot;</span><span>RAG</span></div>
        <div class="hr-footer-copy">Built with LangChain, Chroma &amp; Streamlit</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
