from ui_theme import apply_theme
import streamlit as st
from pathlib import Path
import json
from engine import job_skill_gap
from database import add_job_sources, latest_assessment

ROOT = Path(__file__).resolve().parents[1]
JOBS = json.loads((ROOT/"job_requirements.json").read_text(encoding="utf-8"))
add_job_sources(JOBS)

st.set_page_config(page_title="Your Results | Career Compass", page_icon="🎯", layout="wide")
apply_theme("Your Results")
st.markdown("<div class='cc-hero'><div class='cc-eyebrow'>Your career map</div><h1>Possibilities, meet a plan.</h1><p>Explore your strongest profile matches, see the skills to practise, and turn the next 30 days into tangible progress.</p></div>", unsafe_allow_html=True)
st.caption("PAGE 2 · Career matches, skill gaps, and a practical action plan")

profile = st.session_state.get("profile")
recommendations = st.session_state.get("recommendations")
plan = st.session_state.get("action_plan")
active_student_id = st.session_state.get("student_id")

# Recovery is limited to the active student ID in this browser session. The app
# intentionally never guesses a student by loading the latest local record.
if active_student_id and st.button("↻ Reload saved assessment for this active profile"):
    saved = latest_assessment(active_student_id)
    if saved:
        st.session_state["profile"] = saved["profile"]
        st.session_state["recommendations"] = saved["recommendations"]
        st.session_state["action_plan"] = saved["action_plan"]
        st.session_state["assessment_id"] = saved["assessment_id"]
        st.success("Saved assessment reloaded.")
        st.rerun()
    else:
        st.warning("No saved assessment was found for the active profile in this local database.")
if not profile or recommendations is None or plan is None:
    st.warning("No current assessment in this browser session. Complete the Student Profile page first.")
    if st.button("← Student Profile", type="primary"):
        st.switch_page("app.py")
    st.stop()

if st.button("← Edit my profile"):
    st.switch_page("app.py")

c1,c2,c3 = st.columns(3)
c1.metric("Study level", profile.get("year_label","Not provided"))
c2.metric("Weekly learning time", f"{profile.get('weekly_hours',0)} hours")
c3.metric("Self-reported skills", len(profile.get("skills",[])))
st.caption("The information below is based on your self-reported profile. Project descriptions and task status are not independently verified.")
with st.expander("Profile context used for your guidance"):
    st.write(f"**Python level:** {profile.get('python_skill_level', 'Not assessed')}")
    st.write("**Favourite subjects:** " + (", ".join(profile.get("favorite_subjects", [])) or "Not provided"))
    st.write("**Project experience described:** " + ("; ".join(profile.get("project_experience", [])) or "Not provided"))
    st.caption("Python level, favourite subjects and project descriptions personalise guidance, but they do not currently change the numerical fit score.")

st.header("Your career possibilities")
st.caption("Fit scores reflect profile overlap, not probability of getting hired.")
for i, rec in enumerate(recommendations,1):
    with st.container(border=True):
        st.subheader(f"{i}. {rec['title']} · {rec['fit_score']}% profile fit")
        st.progress(rec["fit_score"]/100)
        st.write(rec.get("description",""))
        st.caption(rec.get("score_note",""))
        left,right = st.columns(2)
        with left:
            st.markdown("**Self-reported skills selected that match**")
            st.write(", ".join(rec.get("matched_skills",[])) or "No direct matches yet.")
            st.markdown("**Why it matched**")
            for reason in rec.get("why_matches",[]): st.write("• "+reason)
        with right:
            st.markdown("**Skills to investigate/practice**")
            st.write(", ".join(rec.get("missing_skills",[])) or "No gaps detected by this comparison.")
            st.markdown("**Suggested starter project**")
            st.write(rec.get("starter_project","Choose a small project relevant to this role."))
        with st.expander("Why this fit score?"):
            st.caption("The score is a weighted profile overlap. The effective weights are renormalised when optional work-style or career-goal inputs are absent.")
            for component in rec.get("score_breakdown", []):
                st.write(f"**{component['component']}** — {component['match_pct']}% overlap · {component['effective_weight_pct']}% effective weight · {component['contribution_points']} points")
        for item in rec.get("guidance",[]): st.info(item)

st.divider()
st.header("Ground your plan in employer evidence")
st.info("This comparison currently contains two dated examples from one employer. It is a small illustration, not a representative labour-market sample or a live vacancy feed.")
for job in JOBS:
    with st.expander(f"{job['role']} — {job['employer']} ({job['checked_on']})"):
        st.write(job["evidence_summary"])
        st.write(f"Experience note: {job['experience_level']}")
        st.markdown(f"[Open original employer posting]({job['source_url']})")
        gap = job_skill_gap(profile,job)
        st.metric("Selected skill overlap", f"{gap['coverage_pct']}%")
        st.write("**Selected matching skills:** "+(", ".join(gap["matched"]) or "None"))
        st.write("**Not reported / not assessed:** "+(", ".join(gap["not_reported_or_unassessed"]) or "None"))
        st.caption("Not reported does not mean you lack the skill. These example postings request prior experience and are not fresher vacancy claims.")

st.divider()
st.header("Your next 30 days")
st.write(plan.get("overview",""))
for week in plan.get("thirty_day_plan",[]):
    with st.expander(f"{week.get('week','Week')} · {week.get('focus','')}"):
        for task in week.get("tasks",[]): st.write("• "+task)
        st.markdown("**Deliverable:** "+week.get("deliverable",""))
for step in plan.get("next_steps",[]): st.write("• "+step)
if plan.get("mode")=="fallback": st.caption("Built-in plan used; no API key required.")
if st.button("Track my progress →", type="primary"):
    st.switch_page("pages/4_My_Progress.py")
