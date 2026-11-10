# AI&DS Career Compass — Master Project Prompt (3.0 and beyond)

Use this as the single source of truth when extending the project. The goal is to improve the existing Streamlit/Python application, not restart from scratch or abandon the older Career Compass work.

## 1. Mission

Build a student-first career-awareness and project-based learning platform specifically for AI & Data Science (AI&DS) students. In plain, compact language, help a student answer:

1. Which skills are useful in real-world work right now?
2. Which skills are currently appearing often in the tracked evidence, and which may become more important over the coming decade?
3. What technology, business, policy, or economic shifts could change the value of a skill?
4. How can a student learn the skill by solving a real problem and proving what they can do?
5. What earnings are reported for jobs using those skills, and what affects the range?
6. What should the student learn or build next, based on their profile and progress?

The core promise is: **learn useful skills, understand why the market values them, practise on realistic problems, and build evidence of ability.** Do not imply that a course or one skill guarantees a job or salary.

## 2. Preserve existing Career Compass functionality

Extend the existing project and keep working features intact unless a change is necessary and tested:

- `app.py`: student profile and home experience.
- `engine.py`, `career_catalog.json`: career recommendations and fit explanation.
- `ai_helper.py`: optional AI-assisted action plan plus no-API-key fallback.
- `job_requirements.json`, `pages/2_Your_Results.py`, `pages/3_Job_Requirements.py`: employer role examples, requirements, and skill-gap comparisons.
- `database.py`, `pages/4_My_Progress.py`: local SQLite profile and progress tracking.
- `pages/5_Demo_Test_Profiles.py`, tests, and existing sample workflows.
- `pages/6_Market_Explorer.py`, `market_signals.json`: searchable skill/market explorer.
- `pages/7_Learning_Studio.py`, `learning_projects.json`: missions, learning paths, and practical challenges.
- `learning_library/`: practice datasets and learning-material notes.

Do not replace, reset, or silently migrate the user’s existing local SQLite database. Back up before schema changes. Keep the older `ai_ds_career_compass_2_0` folder available as a fallback until the user verifies the new version.

## 3. Main product areas

### A. Market Explorer

Build a searchable, filterable area where learners can search a skill (for example Python, SQL, statistics, data engineering, machine learning, deep learning, NLP, MLOps, cloud, or responsible AI) and see:

- A compact one- or two-line explanation of the skill and real-world applications.
- Example AI&DS roles that use it and related skill combinations.
- A clear evidence label: measured posting data, published report, curated qualitative synthesis, or editorial hypothesis.
- Date, source links, geography, role level, and limitations for claims.
- A simple graph that compares only comparable, grounded values. Label the metric and unit. Do not plot qualitative scores as if they were real job-posting counts.
- A “current relevance” view and a separate “possible longer-term outlook” view, with the evidence and uncertainty visible.
- Business, technology, and economic shifts that could affect future demand, with a simple explanation of the mechanism and links to supporting evidence.
- Roles and practical projects that can help a learner build the skill.

Search only the curated dataset unless a separately implemented and tested data source is available. When a skill is not tracked, state that and invite future data collection; never manufacture results. Do not describe the graph as live unless it is actually connected to an actively refreshed, validated source.

### B. Skill economics and earnings

Show earnings by **role, location, experience, employment type, and source**, not a guaranteed fixed pay rate for a standalone skill. Where defensible source data exists, show annual gross salary ranges. Optional monthly, weekly, and hourly equivalents must be labelled as arithmetic conversions of annual gross salary, not advertised wages, take-home pay, or a prediction of the user's income.

For every pay dataset or estimate, store or display the source URL, date, currency, geography, experience band, role, and sample/methodology if known. If a report has no sample size or methodology, disclose that limitation. Separate salaried jobs, internships, freelance contracts, and hourly jobs rather than mixing them. Do not invent missing values.

### C. Market change and outlook

Explain how AI adoption, automation, new regulation, infrastructure investment, industry cycles, cost changes, and shifts in business workflows may change skill needs. For each claim, indicate:

- What changed or is expected to change.
- Which roles or skills may be affected and why.
- Whether the evidence is observed, reported, or a reasoned hypothesis.
- The source and publication date.
- A suitable uncertainty statement and possible alternative outcomes.

Never present a forecast as a fact. Avoid claiming that any skill is certain to rise over the decade. Use clear terms such as “signals suggest”, “possible direction”, or “not enough evidence yet” where appropriate.

### D. Learning Instructor / Learning Studio

Provide guided, step-by-step learning through practical use cases rather than a video/course catalogue alone. Each learning track should include:

- Prerequisites and a short learning objective.
- An explanation in one or two sentences first, with optional deeper detail.
- A small example and a hands-on task.
- A daily mission or next action.
- Checks for understanding, tests, hints, and feedback criteria.
- A way to show progress and return to unfinished work.
- A no-API-key fallback. AI support must not be required for the basic learning workflow.

Daily tasks should be usable in the app. Browser push notifications, email reminders, scheduled background jobs, and cross-device sync are **future features** unless actually implemented and tested. Never claim to send reminders that the app cannot send.

### E. Real-world Project Lab

Teach AI&DS through projects that resemble genuine work: define the problem, inspect data, clean/validate it, establish a baseline, analyse it, test the approach, interpret results, document limitations, and communicate a recommendation.

Every challenge must include:

1. Who has the problem and why it matters.
2. Data source and license/usage notes, or a clear “synthetic practice data” label.
3. Task and expected user workflow.
4. Success criteria and a rubric.
5. Required deliverables (such as code, tests, report, chart, demo, or README).
6. Known limitations, privacy/safety risks, and likely failure modes.
7. A possible extension or next project.
8. Skills the project practises and roles where those skills appear.

Synthetic demo datasets are for practice only and must never be described as evidence of real market demand, real customer behaviour, or real job outcomes. Include projects across AI&DS foundations such as Python, SQL, statistics, data cleaning, visualisation, machine learning, evaluation, deployment, and responsible AI, in a prerequisite-aware order.

### F. Book-grounded learning library

Organise learning references around trusted AI&DS-related books and official/primary documentation, including programming, mathematics, probability, statistics, databases, algorithms, machine learning, deep learning, data engineering, and responsible AI. Use books to guide original summaries, explanations, exercises, and project design.

Record bibliographic details and, where possible, chapter/section references. Do not reproduce full copyrighted chapters, large passages, or entire books. Only ingest uploaded books the user has permission to use, and do not imply a book has been reviewed unless its actual content has been accessed. The platform must also work when no books are uploaded.

## 4. Make the front end feel trustworthy and joyful

The interface should feel welcoming, modern, credible, colourful, and uncluttered—not like a dull administrative form or an exaggerated marketing page.

- Use a warm neutral foundation with restrained indigo/purple, teal, and coral accents.
- Use clear spacing, readable type, good contrast, accessible controls, friendly icons, useful visual hierarchy, and consistent cards.
- Keep home-page explanations short. Show a one- or two-line summary first; place deeper reasoning in expanders or detail sections.
- Make the next action obvious: search a skill, inspect evidence, choose a project, or continue learning.
- Show source and snapshot dates near important market/pay claims.
- Use honest empty states, loading states, and helpful error messages. Do not use invented testimonials, fake user counts, fake placements, fake live indicators, or fabricated success stories.
- Clearly distinguish “self-reported”, “required”, “preferred”, and “demonstrated” skills.
- Explain recommendation scores as profile overlap or fit signals—not probability of getting hired.

## 5. Research and data-quality rules

These rules are mandatory:

- Never invent current vacancies, job-posting counts, salary values, hiring probabilities, demand indexes, citations, or forecasts.
- Separate directly measured observations from third-party published research and editorial synthesis.
- Any vacancy sample must store collection date, source URL, search query or selection method, role, location, experience level, sample size, and duplicate-handling method. Explain that a posting sample is not the entire labour market.
- Keep snapshot dates visible. Dated research is not live data.
- Explain the difference between a skill’s general usefulness and evidence of employer demand for it.
- Show uncertainty and known gaps rather than hiding them.
- When external facts change, refresh sources before presenting them as current.

## 6. Student progress and privacy

- Reuse the existing SQLite progress tracker where possible.
- Let the student add learning challenges to My Progress, view status, and continue unfinished tasks.
- Keep demo/test records clearly separated from real learner data.
- Do not include personal student data, database files, API keys, or secrets in a public repository or ZIP intended for sharing.
- Explain whether data is stored locally or remotely.
- Public deployment requires a separate review of authentication, privacy, persistent database hosting, backups, rate limits, secrets, and data deletion. Do not call a local classroom prototype production-ready.

## 7. Engineering and delivery requirements

- Make small, coherent changes and document which files changed and why.
- Keep existing working features, tests, and no-key fallback.
- Use `requirements.txt` for dependencies and provide a simple Windows launcher (`run_app.bat`) plus clear VS Code instructions.
- Store source-backed market data in a structured data file with schema validation where feasible.
- Keep calculations and business logic separate from the Streamlit presentation layer where reasonably possible.
- Add tests for new logic/data and run the existing test suite after changes.
- Database tests must use temporary databases, never the user's real local database.
- Do not delete user files or migrate the database without an explicit backup plan.
- Verify that the downloadable ZIP contains the complete project and excludes local secrets and user database files.
- Be clear about what was tested. Distinguish compile/unit tests from actually launching and visually checking the website.

## 8. Definition of done

A meaningful release should:

1. Start from a clean extraction using the documented Windows steps.
2. Preserve profile, recommendations, job requirements, and progress features.
3. Allow a user to search tracked skills and understand the meaning and source of market indicators.
4. Display source-dated earnings context without making salary promises.
5. Explain at least one market/economic shift and clearly label uncertainty.
6. Offer a practical learning challenge with data, deliverables, and a rubric.
7. Allow the user to add a challenge to progress tracking and continue later.
8. Keep the no-API-key path working.
9. Pass automated tests, including checks that tests do not modify the user's database.
10. Provide a simple, welcoming user interface and honest documentation of incomplete/future features.

## 9. Working style for the coding assistant

Use short, simple explanations. Do not overwhelm the student with a long essay before performing the work. Make a best-effort implementation in the current project, test it, provide the updated complete folder/ZIP, and state briefly what changed, what passed, and what still needs checking. Never claim a feature is implemented merely because it is described in this prompt.


## Release-hardening additions (2026-11-01)

Before adding features, protect existing student data and verify the complete user workflow. Do not reset or migrate SQLite without a tested backup. Keep local databases, personal records, `.env`, and API secrets out of public ZIPs.

Required implementation safeguards:
- Never auto-select the latest student record when no active profile is present. Use only a profile explicitly created/selected in the current session. State clearly that this is not authentication.
- Validate optional evidence links: blank is allowed; otherwise require a complete HTTP/HTTPS URL, reject credentials embedded in the URL, whitespace, control characters, and excessive length. State that external links are not verified.
- Explain recommendation fit with component-level overlap, effective weights, and contribution points. Do not describe fit as hiring probability. Do not change weights without validation.
- Make contextual use of Python level, favourite subjects, and project descriptions explicit; do not silently mix them into score calculations.
- Label skills and project descriptions as self-reported unless evidence has actually been inspected. A completed task is not automatically verified mastery.
- Display market snapshot date, qualitative signal caveat, salary caveats, synthetic-data labels, and the scope of employer samples near the relevant content.
- If daily mission checkboxes are not persisted, label them session-only.
- Database tests must use temporary database paths and must not create/change `data/career_compass.db`. Connections must always close.
- Any saved-assessment recovery must refer to an explicit active student ID; never recover by choosing the most recent student automatically.

Deferred unless separately researched and tested: real-time scraping, vacancy counts, cross-device sync, production accounts/authentication, automated project grading, measured demand charts, and predictive placement claims.

Latest release-hardening copy (2026-11-01) has 21 passing automated tests and successful Python syntax compilation. Browser visual audit, clean Windows extraction/launch, and manual validation of source links remain pending until performed on the target machine.
