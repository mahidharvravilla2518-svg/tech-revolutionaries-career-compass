import json
from datetime import date
from pathlib import Path

import streamlit as st

from database import add_progress_task, init_db
from ui_theme import apply_theme

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "market_signals.json").read_text(encoding="utf-8"))
PROJECT_DATA = json.loads((ROOT / "learning_projects.json").read_text(encoding="utf-8"))
SEQUENCE_DATA = json.loads((ROOT / "learning_sequences.json").read_text(encoding="utf-8"))
SKILLS = DATA["skills"]
PROJECTS = {project["skill"]: project for project in PROJECT_DATA["projects"]}
SKILL_BY_NAME = {skill["name"]: skill for skill in SKILLS}


def active_local_profile():
    """Use only the profile explicitly created in the current browser session."""
    return st.session_state.get("student_id"), st.session_state.get("assessment_id")

st.set_page_config(page_title="Learning Studio | Career Compass", page_icon="🧪", layout="wide")
apply_theme("Learning Studio")
init_db()

st.markdown("""
<div class="cc-hero cc-hero-learning">
  <div class="cc-eyebrow">Learn by making</div>
  <h1>Less watching.<br>More building.</h1>
  <p>Pick a skill, solve a practical problem, and save your project to your progress tracker.</p>
  <span class="cc-chip">✦ Short daily mission</span><span class="cc-chip">↗ Real-world style challenge</span><span class="cc-chip">✓ Portfolio deliverables</span>
</div>
""", unsafe_allow_html=True)

track_name = st.selectbox("Choose your target skill", [skill["name"] for skill in SKILLS], index=0)
track = next(skill for skill in SKILLS if skill["name"] == track_name)
project = PROJECTS.get(track_name)
pathway = SEQUENCE_DATA["pathways"][track_name]

# Show the broader skill/course order before the daily activity.
st.divider()
st.markdown("## Your learning route")
st.caption("Follow these steps in order. This is a suggested route, not a rigid rule—skip a step you can already demonstrate, and return to it when a project exposes a gap.")
st.markdown(f"### {pathway['title']}")
st.write(pathway["goal"])
path_steps = pathway["steps"]
for index, skill_name in enumerate(path_steps, start=1):
    step_guide = SEQUENCE_DATA["guidance"][skill_name]
    step_project = PROJECTS.get(skill_name)
    is_target = skill_name == track_name
    step_label = "Your selected goal" if is_target else ("Start here" if index == 1 else "Build toward your goal")
    with st.container(border=True):
        num_col, body_col = st.columns([0.55, 7.45])
        with num_col:
            st.markdown(f"<div class='cc-step-number'>{index:02}</div>", unsafe_allow_html=True)
        with body_col:
            if is_target:
                st.markdown(f"### {skill_name} · Your selected goal")
            else:
                st.markdown(f"### {skill_name}")
            st.caption(step_label)
            st.write(step_guide["purpose"])
            st.markdown(f"**Focus:** {step_guide['focus']}")
            st.markdown(f"**Move on when:** {step_guide['ready_when']}")
            if step_project:
                st.caption(f"Practice project: {step_project['title']}")

optional_steps = pathway.get("optional_steps", [])
if optional_steps:
    with st.expander("Optional step for a more specialised route"):
        for optional_skill in optional_steps:
            optional_guide = SEQUENCE_DATA["guidance"][optional_skill]
            st.markdown(f"**{optional_skill}** — {optional_guide['purpose']}")
            st.caption(f"Focus: {optional_guide['focus']}")

next_steps = pathway.get("next_after", [])
if next_steps:
    st.markdown("**After reaching this goal, consider:** " + " · ".join(next_steps))

profile_id, profile_assessment_id = active_local_profile()
if profile_id:
    st.caption(f"This roadmap will be saved to the active local profile #{profile_id}. The app does not authenticate users or sync across devices.")
    if st.button("＋ Add this learning sequence to My Progress", type="primary", use_container_width=True):
        created_count = 0
        already_count = 0
        for step_number, skill_name in enumerate(path_steps, start=1):
            step_project = PROJECTS.get(skill_name, {})
            step_guide = SEQUENCE_DATA["guidance"][skill_name]
            task_title = f"Roadmap: {pathway['title']} · {step_number:02d} {skill_name}"
            task_detail = (
                f"Recommended sequence toward {track_name}. Step {step_number} of {len(path_steps)}. "
                f"Focus: {step_guide['focus']} "
                f"Ready to move on when: {step_guide['ready_when']} "
                f"Suggested practice project: {step_project.get('title', 'Complete a practical exercise')}."
            )
            _, created = add_progress_task(
                profile_id, task_title, task_detail,
                assessment_id=profile_assessment_id, due_week=step_number,
            )
            created_count += int(created)
            already_count += int(not created)
        if created_count:
            st.success(f"Added {created_count} roadmap step(s) to My Progress. " + (f"{already_count} step(s) were already there." if already_count else ""))
        else:
            st.info("This roadmap is already in My Progress. Open that page to update each step's status and evidence link.")
else:
    st.info("No active profile is selected in this browser session. Create a profile assessment here before saving; the app will not choose another local student automatically.")
    if st.button("Create my profile to save progress", key="create_profile_for_roadmap"):
        st.switch_page("app.py")

# Short daily activities are generated in-app; these are not push notifications.
mission_index = (date.today().toordinal() + sum(ord(char) for char in track_name)) % 4
missions = [
    ("Understand the problem", "Write the user's problem in two sentences. Name who experiences it and what a useful result would look like."),
    ("Check the evidence", "Inspect the data source, rows, missing values, and one limitation before drawing conclusions."),
    ("Build one working piece", "Implement one small, testable part. Keep it easy for another student to reproduce."),
    ("Explain what happened", "Show one result, one limitation, and the next action you recommend."),
]
mission_title, mission_detail = missions[mission_index]

left, right = st.columns([1.35, 1])
with left:
    st.markdown("### Today's learning mission")
    with st.container(border=True):
        st.caption(date.today().strftime("%A · %d %B %Y"))
        st.markdown(f"## {mission_title}")
        st.write(mission_detail)
        st.markdown("**Track:** " + track["name"])
        st.checkbox("I completed today's mission", key=f"mission_{date.today().isoformat()}_{track_name}")
        st.caption("This checkbox is session-only and resets with the browser session. Completion is self-reported, not independently verified. Save the project below to keep a task record in My Progress.")
with right:
    st.markdown("### Why this skill matters")
    with st.container(border=True):
        st.write(track["one_line"])
        st.markdown("**Roles that use it**")
        st.write(", ".join(track.get("roles", [])) or "Varies by domain")
        st.markdown("**Current curated signal**")
        st.write(track["current_signal"])
        st.caption(f"Research snapshot: {DATA['meta']['as_of']} · qualitative signal, not live vacancy data.")
        st.caption(track["2030_outlook"])
        st.page_link("pages/6_Market_Explorer.py", label="View the market evidence →", icon="📊")

st.divider()
st.markdown("## Guided path")
st.caption("Small steps. Clear outcomes. Deeper reading is optional.")
for i, step in enumerate(track.get("learning_path", []), 1):
    with st.container(border=True):
        c1, c2 = st.columns([1, 8])
        c1.markdown(f"<div class='cc-step-number'>{i:02}</div>", unsafe_allow_html=True)
        c2.markdown(f"### {step}")
        if i == 1:
            c2.write("Learn the key idea, then explain it in your own words in two lines.")
        elif i == 2:
            c2.write("Practise on a small example. Change one input and explain what changed.")
        elif i == 3:
            c2.write("Apply it to a realistic problem. Record assumptions and mistakes.")
        else:
            c2.write("Package the result with tests, a short README, and a clear explanation of limitations.")

st.divider()
st.markdown("## Your project challenge")
if not project:
    st.warning("A detailed project brief is not available for this track yet. The idea below is a starting point, not a complete assignment.")
    st.markdown(f"**Starter idea:** {track['project']}")
else:
    st.markdown(f"### {project['title']}")
    st.write(project["problem_user"])

    m1, m2 = st.columns(2)
    with m1:
        with st.container(border=True):
            st.markdown("**Your task**")
            st.write(project["task"])
    with m2:
        with st.container(border=True):
            st.markdown("**Data source**")
            st.write(project["data_source_label"])
            dataset_rel = project.get("dataset_file", "")
            dataset_path = (ROOT / dataset_rel).resolve() if dataset_rel else None
            if dataset_path and dataset_path.is_file() and ROOT.resolve() in dataset_path.parents:
                st.download_button(
                    "Download practice dataset",
                    data=dataset_path.read_bytes(),
                    file_name=dataset_path.name,
                    mime="text/csv",
                    key=f"download_{track_name}",
                )
            if project.get("data_source_url"):
                st.markdown(f"[Open data / reference source]({project['data_source_url']})")

    with st.expander("How will this project be evaluated?", expanded=True):
        for criterion in project["success_criteria"]:
            st.markdown(f"- {criterion}")
    st.markdown("**What to submit**")
    cols = st.columns(min(4, len(project["deliverables"])))
    for idx, deliverable in enumerate(project["deliverables"]):
        cols[idx % len(cols)].markdown(f"**{idx + 1}.** {deliverable}")

    with st.expander("Limitations and responsible use"):
        st.write(project["limitations"])
    st.markdown("**Suggested next step**")
    st.write(project["next_step"])

    with st.expander("Book-grounded references"):
        st.caption("These are recommended reading links and topic mappings, not reproduced chapters. Check your edition for exact chapter/page numbers.")
        for resource in project.get("book_resources", []):
            st.markdown(f"- [{resource['title']}]({resource['url']}) — {resource['topic']}")

    # Save only to the profile explicitly created in this browser session.
    student_id, assessment_id = active_local_profile()
    st.divider()
    if student_id:
        st.caption(f"Saving to the active local profile #{student_id}.")
        if st.button("＋ Add this challenge to My Progress", type="primary", use_container_width=True):
            task_id, created = add_progress_task(
                student_id,
                project["title"],
                f"Learning Studio · {track_name}. Start with: {project['task']}",
                assessment_id=assessment_id,
                due_week=1,
            )
            if created:
                st.success("Project added. Open My Progress to update its status and add your portfolio link.")
            else:
                st.info("This project is already in your progress list, so we didn't create a duplicate.")
    else:
        st.info("No active profile is selected. Create a profile assessment in this browser session before saving to My Progress; the app will not choose another local student automatically.")
        if st.button("Create my profile", type="primary"):
            st.switch_page("app.py")

st.divider()
with st.expander("How we use books and learning references"):
    st.write("Career Compass provides original explanations and applied activities grounded in trusted references. It does not reproduce full chapters. When a book is supplied, we can map a specific edition and chapter to short summaries, practice questions, and original project work.")

st.markdown("<div class='cc-footer'>Practice data may be synthetic and is labelled. A completed project is evidence of practice—not a guarantee of employment.</div>", unsafe_allow_html=True)
