
import json
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

import streamlit as st
from engine import recommend_careers
from ai_helper import generate_action_plan
from database import init_db, save_assessment, add_job_sources
from ui_theme import apply_theme

CATALOG = json.loads((ROOT / "career_catalog.json").read_text(encoding="utf-8"))
JOBS = json.loads((ROOT / "job_requirements.json").read_text(encoding="utf-8"))

st.set_page_config(page_title="AI&DS Career Compass 3.0", page_icon="🧭", layout="wide")
apply_theme("Student Profile")
init_db()
add_job_sources(JOBS)


def values(field):
    return sorted({v for c in CATALOG for v in c.get(field, [])}, key=str.lower)


st.markdown("""
<div class="cc-hero">
  <div class="cc-eyebrow">Your next chapter starts here</div>
  <h1>Build skills.<br>Find your direction.</h1>
  <p>A practical career-readiness compass for AI&amp;DS students. Discover paths that fit, understand what employers ask for, and turn learning into proof.</p>
  <span class="cc-chip">✦ Career matches</span><span class="cc-chip">↗ Real job evidence</span><span class="cc-chip">✓ Project portfolio</span>
</div>
""", unsafe_allow_html=True)

st.markdown("## Start with what you want to discover")
st.write("Find the market signal first, then learn by solving a real problem.")

nav1, nav2, nav3 = st.columns(3)

with nav1:
    st.page_link(
        "pages/6_Market_Explorer.py",
        label="Explore skill demand",
        icon="📊",
        help="Search skills, trends, and salary evidence"
    )

with nav2:
    st.page_link(
        "pages/7_Learning_Studio.py",
        label="Open Learning Studio",
        icon="🧪",
        help="Work through daily missions and real-world projects"
    )

with nav3:
    st.page_link(
        "pages/3_Job_Requirements.py",
        label="Check employer evidence",
        icon="🔎",
        help="Inspect source-linked job requirements"
    )

st.markdown("## Let's map your next move")
st.write(
    "Share what you know today. You don't need to have everything "
    "figured out—we'll use your answers to suggest practical next steps."
)

st.info(
    "Employer examples are dated source-linked snapshots, not a live "
    "vacancy feed or a guarantee of hiring outcomes. Some may require "
    "prior experience."
)

st.caption(
    "Your selected skills and project descriptions are self-reported. "
    "Career fit is a profile-overlap guide, not a hiring prediction."
)

with st.form("profile_form"):
    name = st.text_input("Display name (optional)")

    year = st.selectbox(
        "Year of study",
        ["1st year", "2nd year", "3rd year", "4th year", "Recent graduate"],
        index=1
    )

    python_level = st.select_slider(
        "Python level",
        options=["Not assessed", "Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )

    skill_options = sorted(
        set(values("required_skills") + [
            "Excel", "Git", "NumPy", "pandas", "data structures",
            "communication", "Power BI", "problem solving"
        ]),
        key=str.lower
    )

    skills = st.multiselect(
        "Skills you currently identify as able to demonstrate",
        skill_options,
        help="Self-reported by you; the application does not independently verify proficiency."
    )

    interest_options = sorted(
        set(values("interests") + [
            "machine learning", "statistics", "data analysis",
            "technology", "team projects", "visualization",
            "business problem solving"
        ]),
        key=str.lower
    )

    interests = st.multiselect("Interests", interest_options)

    subjects = st.multiselect(
        "Favorite subjects",
        [
            "Programming", "Mathematics", "Statistics", "DBMS",
            "AI/ML", "Data Science", "Business"
        ]
    )

    project_text = st.text_area(
        "Projects or practical work (optional)",
        placeholder="Example: cleaned a public CSV and made three charts",
        help=(
            "Describe work you have done. A description alone is not "
            "independently verified evidence; add a repository or demo "
            "link to your progress record when available."
        )
    )

    target = st.selectbox(
        "Career goal",
        ["Not sure yet"] + [c["title"] for c in CATALOG]
    )

    work = st.selectbox(
        "Preferred work style",
        [
            "analyzing data",
            "business problem solving",
            "building software",
            "building AI models",
            "mathematics and research"
        ]
    )

    hours = st.slider("Learning hours per week", 1, 20, 5)

    submitted = st.form_submit_button(
        "✨ Build my career map",
        type="primary",
        use_container_width=True
    )


if submitted:
    year_num = {
        "1st year": 1,
        "2nd year": 2,
        "3rd year": 3,
        "4th year": 4,
        "Recent graduate": 4
    }[year]

    profile = {
        "display_name": name.strip(),
        "year": year_num,
        "year_label": year,
        "python_skill_level": python_level,
        "skills": skills,
        "interests": interests,
        "favorite_subjects": subjects,
        "project_experience": [
            x.strip() for x in project_text.splitlines() if x.strip()
        ],
        "target_career": None if target == "Not sure yet" else target,
        "preferred_work": work,
        "weekly_hours": hours
    }

    with st.spinner("Matching your profile and preparing a learning plan..."):
        recommendations = recommend_careers(profile, CATALOG, top_n=3)
        plan = generate_action_plan(profile, recommendations)
        student_id, assessment_id = save_assessment(
            profile, recommendations, plan
        )

    st.session_state["profile"] = profile
    st.session_state["recommendations"] = recommendations
    st.session_state["action_plan"] = plan
    st.session_state["student_id"] = student_id
    st.session_state["assessment_id"] = assessment_id

    st.success("Your profile is saved. Let's explore your career map…")
    st.switch_page("pages/2_Your_Results.py")


with st.sidebar:
    st.markdown("## 🧭 Career Compass")
    st.write("1. Student Profile")
    st.write("2. Your Results")
    st.write("3. Job Requirements")
    st.write("4. My Progress")
    st.write("5. Demo Test Profiles")
    st.write("6. Market Explorer")
    st.write("7. Learning Studio")
    st.divider()
    st.caption(
        "A student-focused prototype · Local demo data only. "
        "Avoid entering sensitive personal information."
    )
