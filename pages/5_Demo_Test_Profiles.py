from ui_theme import apply_theme
import json, streamlit as st
from pathlib import Path
st.set_page_config(page_title="Demo Test Profiles | Career Compass", page_icon="🧪", layout="wide")
apply_theme("Demo Test Profiles")
ROOT=Path(__file__).resolve().parents[1]
profiles=json.loads((ROOT/"test_profiles.json").read_text(encoding="utf-8"))
st.markdown("<div class='cc-hero'><div class='cc-eyebrow'>Quality check</div><h1>Test the compass.</h1><p>Use demo profiles to check whether recommendations behave sensibly across different student starting points.</p></div>", unsafe_allow_html=True)
st.caption("Page 5 · Five fictional test cases")
st.info("These are fictional fixtures, not real students. This page displays them for manual testing; it does not submit them or save them to the database.")
for p in profiles:
    with st.expander(f"{p['profile_id']} · {p.get('student_name') or 'Incomplete profile'}"):
        st.write(f"**Scenario:** {p.get('notes','')}")
        st.write(f"**Year:** {p.get('year_of_study') or 'Not provided'}")
        st.write(f"**Python level:** {p.get('python_skill_level') or 'Not assessed'}")
        st.write(f"**Skills:** {', '.join(p.get('skills',[])) or 'None provided'}")
        st.write(f"**Interests:** {', '.join(p.get('interests',[])) or 'None provided'}")
        st.write(f"**Career goal:** {p.get('career_goal') or 'Not specified'}")
        st.write(f"**Project experience:** {', '.join(p.get('project_experience',[])) or 'None provided'}")
        if p.get("missing_fields"): st.write("**Missing fields:** "+", ".join(p["missing_fields"]))
