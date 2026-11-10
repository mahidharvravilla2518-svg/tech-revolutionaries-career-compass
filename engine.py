"""Career matching and evidence-aware skill-gap utilities."""
import re
from urllib.parse import urlsplit

ALIASES = {
    "basic sql": "sql", "sql basics": "sql", "python basics": "python",
    "basic python syntax": "python", "numpy basics": "numpy", "pandas basics": "pandas",
    "descriptive statistics": "statistics", "data analysis": "data analysis",
    "visualization": "data visualization", "charts": "data visualization",
    "machine learning": "machine learning", "ml": "machine learning",
    "git basics": "git", "basic data structures": "data structures",
    "if/else": "control flow", "loops": "control flow", "variables": "programming basics"
}


def normalise(value):
    s = re.sub(r"\s+", " ", str(value or "").strip().lower())
    return ALIASES.get(s, s)


def _values(profile, key):
    value = profile.get(key, [])
    if value is None:
        return set()
    if isinstance(value, str):
        value = [value]
    try:
        return {normalise(v) for v in value if str(v).strip()}
    except TypeError:
        return set()


def _overlap(required, known):
    required_norm = {normalise(x) for x in required}
    if not required_norm:
        return 0.0, set(), set()
    matched = required_norm & known
    missing = required_norm - known
    return len(matched) / len(required_norm), matched, missing


def recommend_careers(profile, catalog, top_n=3):
    """Return provisional profile-fit recommendations with transparent components."""
    if not isinstance(profile, dict):
        profile = {}
    if not isinstance(catalog, (list, tuple)):
        raise TypeError("catalog must be a list or tuple of career records")
    try:
        top_n = max(0, int(top_n))
    except (TypeError, ValueError):
        raise ValueError("top_n must be a non-negative integer")

    skills = _values(profile, "skills")
    interests = _values(profile, "interests")
    work = _values(profile, "preferred_work")
    goal = normalise(profile.get("target_career") or profile.get("career_goal") or "")
    has_goal = bool(goal and goal not in {"not sure yet", "none", "null"})
    python_level = str(profile.get("python_skill_level") or "Not assessed").strip()
    favourite_subjects = profile.get("favorite_subjects") or []
    if isinstance(favourite_subjects, str):
        favourite_subjects = [favourite_subjects]
    project_experience = profile.get("project_experience") or []
    if isinstance(project_experience, str):
        project_experience = [project_experience] if project_experience.strip() else []
    year = profile.get("year", profile.get("year_of_study"))
    hours = profile.get("weekly_hours", 5)
    try:
        hours = max(1, min(168, int(hours)))
    except (TypeError, ValueError):
        hours = 5

    results = []
    for career in catalog:
        required_skills = career.get("required_skills", [])
        required_interests = career.get("interests", [])
        skill_score, matched_skills, missing_skills = _overlap(required_skills, skills)
        interest_score, matched_interests, _ = _overlap(required_interests, interests)
        work_score, _, _ = _overlap(career.get("work_types", []), work)
        title = normalise(career.get("title", ""))
        goal_match = bool(has_goal and (goal in title or title in goal))

        components = [("Skills", skill_score, .4), ("Interests", interest_score, .4)]
        if work:
            components.append(("Preferred work style", work_score, .1))
        if has_goal:
            components.append(("Career goal", 1.0 if goal_match else 0.0, .1))
        total_weight = sum(weight for _, _, weight in components)
        breakdown = [
            {
                "component": label,
                "match_pct": round(score * 100),
                "effective_weight_pct": round(weight / total_weight * 100, 1),
                "contribution_points": round(score * weight / total_weight * 100, 1),
            }
            for label, score, weight in components
        ]
        # Keep the displayed one-decimal weights summing to exactly 100.0.
        if breakdown:
            rounded_total = sum(item["effective_weight_pct"] for item in breakdown)
            breakdown[-1]["effective_weight_pct"] = round(
                breakdown[-1]["effective_weight_pct"] + (100.0 - rounded_total), 1
            )
        fit = round(100 * sum(score * weight for _, score, weight in components) / total_weight) if total_weight else 0

        why = []
        if matched_skills:
            why.append("Your selected skills overlap with this career's skill guide.")
        if matched_interests:
            why.append("Your interests overlap with this career's typical work.")
        if goal_match:
            why.append("This matches the career you said you want to explore.")
        if not why:
            why.append("Treat this as an exploration option; add more profile details to improve the match.")

        guidance = []
        if not skills:
            guidance.append("Your skill profile is incomplete; begin with one foundational skill and reassess.")
        elif year in (1, 2) or str(year) in ("1", "2"):
            guidance.append("Build foundations and complete one small project before specializing.")
        else:
            guidance.append("Build a portfolio project that demonstrates the core skills for this path.")
        if python_level.lower() in {"beginner", "not assessed", ""}:
            guidance.append(f"Python level recorded as {python_level or 'Not assessed'}; use beginner-friendly exercises before increasing project complexity.")
        elif "python" in {normalise(skill) for skill in required_skills}:
            guidance.append(f"Python level recorded as {python_level}; choose project complexity that matches your current confidence.")
        if favourite_subjects:
            guidance.append("Use your favourite subjects (" + ", ".join(str(x) for x in favourite_subjects[:4]) + ") as context for project ideas; they do not change the fit score.")
        if project_experience:
            guidance.append("You described prior practical work. Add a repository, demo, report, or other artifact before treating it as externally verified evidence.")
        else:
            guidance.append("No project experience was entered; start with the suggested project and save an artifact when ready.")
        guidance.append(f"Plan around {hours} learning hour(s) per week; keep tasks small enough to finish.")

        score_note = "Fit score is a profile-overlap indicator, not a hiring probability or placement prediction."
        if not skills and not interests and not work and not has_goal:
            score_note += " This is a low-information provisional result because no matching profile inputs were supplied."

        results.append({
            **career,
            "fit_score": fit,
            "score_breakdown": breakdown,
            "why_matches": why,
            "matched_skills": sorted(matched_skills),
            "matched_interests": sorted(matched_interests),
            "missing_skills": sorted(missing_skills),
            "guidance": guidance,
            "score_note": score_note,
        })
    return sorted(results, key=lambda item: item["fit_score"], reverse=True)[:top_n]


def validate_evidence_url(value, max_length=2048):
    """Allow blank optional links or syntactically valid HTTP(S) URLs only."""
    raw = str(value or "").strip()
    if not raw:
        return True, ""
    if len(raw) > max_length:
        return False, f"Link must be {max_length} characters or fewer."
    if any(char.isspace() or ord(char) < 32 for char in raw):
        return False, "Link must not contain spaces or control characters."
    try:
        parsed = urlsplit(raw)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return False, "Use a complete link beginning with http:// or https://."
        _ = parsed.port  # Accessing port validates malformed port values.
    except ValueError:
        return False, "Enter a valid HTTP or HTTPS link."
    if parsed.username or parsed.password:
        return False, "Links containing embedded usernames or passwords are not accepted."
    return True, ""


def job_skill_gap(profile, job):
    """Return evidence-aware skill gap; unreported skills are unknown, not automatically absent."""
    profile = profile if isinstance(profile, dict) else {}
    known = _values(profile, "skills")
    required = {normalise(x) for x in job.get("required_skills", [])}
    matched = sorted(required & known)
    unassessed = sorted(required - known)
    return {
        "matched": matched,
        "not_reported_or_unassessed": unassessed,
        "coverage_pct": round(100 * len(matched) / len(required)) if required else 0,
    }
