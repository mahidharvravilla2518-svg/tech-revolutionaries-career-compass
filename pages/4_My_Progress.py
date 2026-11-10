import streamlit as st
from ui_theme import apply_theme
from database import get_tasks, update_task
from engine import validate_evidence_url

st.set_page_config(page_title="My Progress | Career Compass", page_icon="📈", layout="wide")
apply_theme("My Progress")
st.markdown("<div class='cc-hero'><div class='cc-eyebrow'>Small steps add up</div><h1>Your progress, clearly tracked.</h1><p>Track practical work, attach evidence, and build a portfolio you can explain—not just a list of things you've studied.</p></div>", unsafe_allow_html=True)

sid = st.session_state.get("student_id")
if not sid:
    st.info("No active profile is selected in this browser session. For privacy, this page will not automatically open the latest local student record.")
    if st.button("← Open Student Profile", type="primary"):
        st.switch_page("app.py")
    st.stop()

tasks = get_tasks(sid)
st.caption(f"ACTIVE LOCAL PROFILE #{sid} · Task status and evidence are stored on this computer. This prototype has no account authentication or cross-device sync.")
st.info("Task status and evidence links are learner-reported. Marking a task complete does not independently verify skill mastery.")
if not tasks:
    st.info("No starter projects are attached to this assessment yet.")
else:
    completed = sum(1 for task in tasks if task.get("status") == "Completed")
    in_progress = sum(1 for task in tasks if task.get("status") == "In progress")
    c1,c2,c3 = st.columns(3)
    c1.metric("Projects completed", f"{completed}/{len(tasks)}")
    c2.metric("In progress", in_progress)
    c3.metric("Still to start", len(tasks)-completed-in_progress)
    st.progress(completed/len(tasks), text=f"{round(completed/len(tasks)*100)}% of starter projects completed")
    st.markdown("## Your project workspace")
    st.caption("Update a project's status and optionally attach a GitHub repository or demo URL.")
    for idx,task in enumerate(tasks,1):
        with st.container(border=True):
            st.markdown(f"### {idx:02d} · {task['task_title']}")
            st.caption(task.get("task_detail") or "Practical starter project")
            status_options=["Not started","In progress","Completed"]
            current=task.get("status","Not started")
            if current not in status_options: current="Not started"
            left,right=st.columns([1,2])
            with left:
                status=st.selectbox("Project status",status_options,index=status_options.index(current),key=f"status_{task['id']}")
            with right:
                evidence=st.text_input("Evidence link (optional)",value=task.get("evidence_url") or "",key=f"url_{task['id']}",placeholder="https://github.com/your-project")
            st.caption("External links are not verified by Career Compass. Use only a repository or demo URL you are comfortable sharing.")
            if st.button("Save project update",key=f"save_{task['id']}",type="primary"):
                valid, message = validate_evidence_url(evidence)
                if not valid:
                    st.error(message)
                else:
                    update_task(task["id"],status,evidence.strip())
                    st.success("Project update saved.")
                    st.rerun()
st.markdown("<div class='cc-footer'>Local SQLite prototype · Not secure multi-user storage. Do not deploy publicly or enter sensitive personal information.</div>", unsafe_allow_html=True)
