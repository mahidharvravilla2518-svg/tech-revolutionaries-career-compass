"""Optional AI plan generation; reliable local fallback works without an API key."""
import os, json

def fallback_plan(profile, recommendations, reason="AI API not configured"):
    top = recommendations[0] if recommendations else {}
    role = top.get("title", "career exploration")
    missing = top.get("missing_skills", [])[:4]
    hours = profile.get("weekly_hours", 5)
    week_tasks = [
      {"week":"Week 1","focus":"Foundations and baseline","tasks":[f"Spend {max(1, hours//2)} hours revising one core skill for {role}.","Write down what you can already do and what is still unclear."],"deliverable":"A short baseline checklist."},
      {"week":"Week 2","focus":"Practice the main skill gap","tasks":[f"Practice: {', '.join(missing[:2]) if missing else 'the core skills listed for the chosen role'}.","Complete 3 small exercises and note mistakes."],"deliverable":"A practice notebook or short notes."},
      {"week":"Week 3","focus":"Build a portfolio artifact","tasks":[top.get("starter_project","Choose a small role-relevant project and define its outcome."),"Use a public or synthetic dataset; do not upload private student data."],"deliverable":"A working project draft with README."},
      {"week":"Week 4","focus":"Validate and explain your work","tasks":["Test the project on at least 3 cases and record limitations.","Write a short explanation of the problem, method, results, and next improvement."],"deliverable":"A project demo or repository link."}
    ]
    return {"overview":f"Starter plan for exploring {role}. This is guidance, not a job guarantee.",
            "thirty_day_plan":week_tasks,
            "next_steps":["Choose one target role to investigate further.","Compare this plan with at least one dated employer posting.","Review progress after 30 days."],
            "limitations":[reason, "Job requirements vary by employer and seniority."],
            "mode":"fallback"}

def generate_action_plan(profile, recommendations):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return fallback_plan(profile, recommendations)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-5.5")
        payload = {"profile": profile, "recommendations": [
            {"title": r.get("title"), "missing_skills": r.get("missing_skills", []),
             "starter_project": r.get("starter_project")} for r in recommendations[:3]
        ]}
        response = client.responses.create(
            model=model,
            input=[
              {"role":"system","content":"Create a realistic 4-week student learning plan. Return only valid JSON with keys overview, thirty_day_plan (4 objects with week, focus, tasks list, deliverable), next_steps (list), limitations (list), mode='ai'. Do not promise employment. Be beginner-aware and concise."},
              {"role":"user","content":json.dumps(payload, ensure_ascii=False)}
            ]
        )
        text = response.output_text
        data = json.loads(text)
        if not isinstance(data, dict) or not isinstance(data.get("thirty_day_plan"), list):
            raise ValueError("AI response did not match expected plan format")
        data["mode"] = "ai"
        return data
    except Exception as exc:
        return fallback_plan(profile, recommendations, f"AI request failed; fallback used ({type(exc).__name__}).")
