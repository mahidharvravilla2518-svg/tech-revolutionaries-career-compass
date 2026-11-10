from ui_theme import apply_theme
import json, streamlit as st
from pathlib import Path
from database import add_job_sources
ROOT=Path(__file__).resolve().parents[1]
JOBS=json.loads((ROOT/"job_requirements.json").read_text(encoding="utf-8"))
add_job_sources(JOBS)
st.set_page_config(page_title="Job Requirements | Career Compass", page_icon="🔎", layout="wide")
apply_theme("Job Requirements")
st.markdown("<div class='cc-hero'><div class='cc-eyebrow'>Evidence over guesswork</div><h1>What do employers ask for?</h1><p>Explore source-linked job requirements and use them as evidence—not as universal rules for every role.</p></div>", unsafe_allow_html=True)
st.caption("PAGE 3 · Source-linked job evidence")
st.warning("Small dated sample: two Amazon postings from one employer, checked on the dates shown. This is not a representative market sample or live vacancy feed. A posting may close or change; reopen the original link before describing it as currently open. Not reported does not mean an employer does not value a skill.")
for job in JOBS:
    with st.container(border=True):
        st.subheader(f"{job['role']} — {job['employer']}")
        st.write(f"**Location:** {job.get('location','Not listed')} · **Checked on:** {job['checked_on']}")
        st.write(f"**Seniority:** {job['experience_level']}")
        st.write(job["evidence_summary"])
        st.markdown("**Required skills listed**")
        st.write(", ".join(job.get("required_skills",[])))
        st.markdown("**Preferred skills listed**")
        st.write(", ".join(job.get("preferred_skills",[])))
        st.markdown(f"[Open original employer posting]({job['source_url']})")
        st.caption(job["limitations"])
st.info("Current sample size: two employer postings from one employer. Do not generalize this to the entire job market. Next research task: add fresh/intern/graduate postings from several employers.")
