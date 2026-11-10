import json
from pathlib import Path

import pandas as pd
import streamlit as st

from ui_theme import apply_theme

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "market_signals.json").read_text(encoding="utf-8"))
SKILLS = DATA["skills"]
ROLES = DATA["roles"]
SOURCES = {source["id"]: source for source in DATA["sources"]}

st.set_page_config(page_title="Market Explorer | Career Compass", page_icon="📊", layout="wide")
apply_theme("Market Explorer")

st.markdown("""
<div class="cc-hero cc-hero-market">
  <div class="cc-eyebrow">Curiosity meets evidence</div>
  <h1>Explore the skills<br>the world is moving toward.</h1>
  <p>Search a skill. Explore a dated market snapshot, longer-term outlook, real applications, and salary context for related roles.</p>
  <span class="cc-chip">✦ Source-linked research</span><span class="cc-chip">↗ Skill outlook</span><span class="cc-chip">₹ Pay context</span>
</div>
""", unsafe_allow_html=True)

meta = DATA["meta"]
st.info(f"Research snapshot: {meta['as_of']} · Signal scores are qualitative 1–5 synthesis, not vacancy counts, live demand or hiring probabilities.")
left, right = st.columns([2, 1])
with left:
    query = st.text_input("Search any skill", placeholder="Try Python, SQL, cybersecurity, LLMs, data storytelling…", help="Search names, aliases, tools, or related roles. Unknown skills are not assigned an invented demand score.")
with right:
    view = st.selectbox("Explore", ["All tracked skills", "Strong growth signals", "Core foundations", "Sector-linked opportunities"])


def matches_query(skill, text):
    if not text.strip():
        return True
    haystack = " ".join([skill["name"], skill.get("current_signal", ""), skill.get("2030_outlook", ""), skill.get("one_line", ""), *skill.get("aliases", []), *skill.get("roles", [])]).lower()
    return text.lower().strip() in haystack

filtered = [s for s in SKILLS if matches_query(s, query)]
if view == "Strong growth signals":
    filtered = [s for s in filtered if s["signal_score"] >= 5]
elif view == "Core foundations":
    filtered = [s for s in filtered if s["name"] in {"Programming Fundamentals", "SQL and Database Skills", "Statistics and Experimentation", "Data Analysis and Storytelling"}]
elif view == "Sector-linked opportunities":
    filtered = [s for s in filtered if s["name"] in {"Green and Energy Data", "Cybersecurity and Risk", "LLMs and Generative AI"}]

if not filtered:
    st.warning("We don't have a verified signal for that search in this prototype yet. We won't guess. Try a broader term, or use the source links below to research it and add it to the library.")
else:
    chart_data = pd.DataFrame([{"Skill": s["name"], "Signal score": s["signal_score"]} for s in filtered]).set_index("Skill")
    st.markdown("### Market signal map")
    st.caption(f"Qualitative synthesis · Snapshot: {meta['as_of']} · Coverage: {meta.get('market', 'Not specified')} · Not live job-posting counts.")
    st.bar_chart(chart_data, height=min(460, 95 + 34 * len(chart_data)))

    selected_name = st.selectbox("Open a skill", [s["name"] for s in filtered])
    selected = next(s for s in filtered if s["name"] == selected_name)
    a, b, c = st.columns(3)
    a.metric("Market signal", f"{selected['signal_score']}/5", selected["current_signal"])
    b.metric("Longer-term outlook", "Through 2030")
    c.metric("Evidence links", str(len(selected.get("evidence", []))) if selected.get("evidence") else "Role-based")

    with st.container(border=True):
        st.subheader(selected["name"])
        st.write(selected["one_line"])
        st.markdown(f"**Now:** {selected['current_signal']}  ")
        st.markdown(f"**Outlook:** {selected['2030_outlook']}")
        st.markdown("**Roles that use it:** " + (", ".join(selected.get("roles", [])) or "Depends on domain and job description"))
        st.markdown("**A project you can build:** " + selected["project"])
        if selected.get("evidence"):
            st.markdown("**Evidence behind this signal**")
            for source_id in selected["evidence"]:
                source = SOURCES[source_id]
                st.markdown(f"- [{source['publisher']}: {source['title']}]({source['url']})")
        else:
            st.caption("This is described as a core role skill from the project’s role taxonomy, not as a measured fast-growing trend. Add specific job-posting evidence before making a growth claim.")

    related_roles = []
    desired_ids = set(selected.get("salary_role_ids", []))
    related_roles = [role for role in ROLES if role["id"] in desired_ids]
    if related_roles:
        st.markdown("### What jobs using this skill may pay")
        st.caption("Pay belongs to a role and experience level—not to a skill by itself. Figures below are source-reported ranges; monthly, weekly and hourly values are arithmetic equivalents, not advertised hourly rates or take-home pay.")
        for role in related_roles:
            with st.container(border=True):
                st.markdown(f"#### {role['name']}")
                st.write(f"**Experience basis:** {role['experience']}")
                pay = st.columns(4)
                low, high = role["low_lpa"], role["high_lpa"]
                pay[0].metric("Annual gross equivalent", f"₹{low:g}–{high:g} LPA")
                pay[1].metric("Monthly equivalent", f"₹{low*100000/12/1000:.0f}k–₹{high*100000/12/1000:.0f}k")
                pay[2].metric("Weekly equivalent", f"₹{low*100000/52/1000:.1f}k–₹{high*100000/52/1000:.1f}k")
                pay[3].metric("Hourly equivalent", f"₹{low*100000/2080:.0f}–₹{high*100000/2080:.0f}")
                source = SOURCES[role["source_id"]]
                st.caption(role["pay_label"] + f" · Source: {source['publisher']}, {source['published']}")
                st.write(role["caveat"])
                st.markdown(f"[Open salary source]({source['url']})")
    else:
        st.info("This skill has no role-level salary band in the current snapshot. That is intentional: we won't assign a pay amount to a skill without a suitable salary source.")

    st.markdown("### A practical learning path")
    for i, step in enumerate(selected.get("learning_path", []), 1):
        st.markdown(f"**{i}.** {step}")
    st.page_link("pages/7_Learning_Studio.py", label="Learn this through a real-world challenge →", icon="🧪")

st.divider()
st.markdown("## What is changing in the economy?")
for shift in DATA["economic_shifts"]:
    with st.container(border=True):
        st.markdown(f"### {shift['title']}")
        st.write(shift["signal"])
        st.caption(shift["student_meaning"])
        for source_id in shift["source_ids"]:
            source = SOURCES[source_id]
            st.markdown(f"[Read: {source['publisher']} — {source['title']}]({source['url']})")

with st.expander("How to read our market data"):
    st.write(meta["method_note"])
    st.write(f"**Snapshot date:** {meta['as_of']} · **Coverage:** {meta['market']}")
    st.write("This version does not yet scrape job boards or count current vacancies. Demand and outlook are qualitative signals drawn from the dated sources below. The next research upgrade should add a repeatable sample of current listings across several employers, locations and experience levels.")
    for source in DATA["sources"]:
        st.markdown(f"- [{source['title']}]({source['url']}) — {source['scope']}")

st.markdown("<div class='cc-footer'>Explore with curiosity. Decide with evidence. Pay varies by employer, location, experience, skills, and market conditions.</div>", unsafe_allow_html=True)
