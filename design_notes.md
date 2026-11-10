# AI&DS Career Compass 3.0 — design and product direction

## Visual identity
- Warm off-white background, indigo/purple primary, teal progress accent, coral highlights.
- Manrope headings and DM Sans body text; rounded cards; generous spacing; accessible contrast.
- Friendly, hopeful language without promising jobs or overstating AI.
- Consistent shared theme in `ui_theme.py` across all Streamlit pages.

## Product principles
1. Recommendations are profile-match guidance, not hiring probabilities.
2. Employer requirements must be source-linked and dated; sample postings are not market-wide evidence.
3. Distinguish self-selected skills from demonstrated skills.
4. Every career suggestion should connect to a practical deliverable and a way to show evidence.
5. Validate usefulness with students and, when possible, employers before making strong claims.

## Next real-world validation steps
- Expand source-linked examples across multiple employers and junior/internship/graduate roles.
- Capture source date, role seniority, location, and required vs preferred skills.
- Ask students to assess whether recommendations and projects are relevant and feasible.
- Add project rubrics and evidence-based skill confirmation.


## Learning Studio project-spec upgrade (2026-10-27)

- Added `learning_projects.json`, with a structured project brief for each skill in `market_signals.json`.
- Briefs state the problem/user, data source, task, success criteria, deliverables, limitations, next step, and references.
- Added small CSV practice datasets. They are synthetic and must not be used as evidence about actual companies, people, market demand, or energy output.
- Learning Studio can add a chosen challenge to the local `progress_tasks` table. Duplicate titles are not added twice for the same student record.
- Automated tests now use a temporary SQLite database so test runs do not put `TEST ONLY` rows into a student's live project database.


## Ordered learning routes
The Learning Studio now recommends a step-by-step skill sequence for every tracked target, showing what to focus on, how to recognise readiness, optional branches, and sensible follow-on skills. The whole sequence can be saved to the existing local progress tracker; this is a recommendation, not a rigid prerequisite rule.


## Release-hardening decisions (2026-11-01)

- Do not auto-select the most recent local student record in My Progress or Learning Studio. Use only the active profile created in the current browser session.
- Treat the session record ID as a navigation aid, not authentication. The app remains a local single-user prototype.
- Label profile skills and project descriptions as self-reported. A task status is not independent proof of mastery.
- Explain the existing profile-fit score using its weighted components; do not change the scoring weights without separate validation.
- Use Python level, favourite subjects, and project descriptions to contextualise learning guidance, not to silently alter the fit score.
- Accept only blank optional evidence links or syntactically valid HTTP/HTTPS URLs. Warn that external links are not verified.
- Display market snapshot date and qualitative-score caveats prominently; display the two-posting/one-employer limitation near job examples.
- Keep daily mission completion labelled session-only until durable persistence is implemented and tested.
- The current update does not add live scraping, accounts, cloud sync, automated project grading, or new market claims.
