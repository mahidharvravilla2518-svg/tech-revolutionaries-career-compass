# AI&DS Career Compass 3.0

**A student-first career and learning compass:** understand useful skills, explore market signals, learn through real-world projects, and view salary evidence for related roles.

## What's new

- **Market Explorer:** search a tracked skill, view its evidence signal, current relevance, outlook through 2030, related roles, project ideas, economic shifts, and sourced salary context.
- **Learning Studio:** short daily missions, recommended skill/course order from foundations to a chosen goal, focus and readiness checks at each step, optional specialisation branches, complete project briefs, downloadable practice datasets, book-grounded references, and actions to save a single challenge or the full route to My Progress.
- **Updated visual design:** warm cream surfaces, indigo/teal accents, friendly cards, short explanations, and direct navigation.
- **Existing Career Compass features retained:** profile assessment, career recommendations, skill-gap comparison, optional AI/fallback action plan, and SQLite progress tracking.

## Start on Windows

1. Extract this ZIP into a **new folder** named `AI_DS_Career_Compass_3_0`.
2. For the easiest start, double-click **`run_app.bat`**. It uses the Python location previously identified on your computer and installs requirements if Streamlit is missing.
3. Or open the folder in VS Code (`File` → `Open Folder`), choose `Terminal` → `New Terminal`, and run the commands below one at a time:

```powershell
& "$env:LocalAppData\Python\pythoncore-3.14-64\python.exe" -m pip install -r requirements.txt
& "$env:LocalAppData\Python\pythoncore-3.14-64\python.exe" -m streamlit run app.py
```

The terminal will show a local address, usually `http://localhost:8501`. Open it in your browser. If another Streamlit app is already running on that port, stop it with `Ctrl+C` in its terminal first.

## Data integrity: please read

- Keep your existing `ai_ds_career_compass_2_0` folder. This is a **new working copy**, not a replacement.
- The archive available for this build did not include the live SQLite database from your laptop. This copy will create its own `data/career_compass.db`; old local records remain in the old folder.
- Do not delete the old folder until you have checked both versions and backed up any database you care about.

## Market-data integrity

`market_signals.json` was assembled from sources checked for this build, with a snapshot date of 27 October 2026. It is **not live job-board data**. Search works within the curated library; a skill not yet tracked will say so rather than invent a score. The chart's 1–5 score is a qualitative evidence synthesis, not vacancy volume or the probability of a job offer.

Salary figures belong to roles, not individual skills. The app shows cited ranges and calculates annual-to-monthly, weekly and hourly equivalents for context. These calculations are not take-home pay or quoted hourly contract rates. Sample, location, experience level and source date matter. Always re-open original sources before using figures in a formal presentation.

## Core files

- `app.py` — profile form and home navigation.
- `engine.py` — recommendation logic and explainable fit scores.
- `ai_helper.py` — optional AI-generated action plan and fallback mode.
- `database.py` — local SQLite persistence.
- `career_catalog.json` — career guides and starter projects.
- `job_requirements.json` — source-linked employer role examples.
- `market_signals.json` — tracked skills, trends, salary references, sources and economic-shift notes.
- `pages/6_Market_Explorer.py` — searchable market research and pay context.
- `pages/7_Learning_Studio.py` — daily in-app mission and project-led learning.
- `learning_projects.json` — structured challenge briefs for every tracked skill.
- `learning_sequences.json` — recommended learning order for every tracked skill, with focus points, readiness checks, optional branches, and suggested next steps.
- `learning_library/datasets/` — small synthetic practice datasets, clearly labelled as fictional.
- `BUILD_PROMPT.md` — reusable prompt for future safe upgrades.
- `run_app.bat` — convenient Windows launcher.
- `docs/PROJECT_CONTINUITY.md` — migration, research and privacy notes.

## Tests

Run from this folder:

```powershell
& "$env:LocalAppData\Python\pythoncore-3.14-64\python.exe" -m unittest discover -s tests -v
```

## Important current limitations

- Market signals are a curated dated snapshot; the app does not scrape job boards or show live vacancy counts.
- Daily missions appear when the page is opened. Push reminders and cross-device sync are not implemented. The daily mission checkbox is session-level; adding a full project to My Progress is stored in local SQLite.
- Learning content is original and guided by reference links; automatic book ingestion is not implemented yet. Project briefs include the problem, source, task, success criteria, deliverables, limitations, and next step. Ordered learning routes are recommendations and can be adapted when a learner can already demonstrate a step.
- The app is a local classroom prototype, not secure multi-user production software.


## Release-hardening updates (1 November 2026)

- **Safer local progress access:** My Progress and Learning Studio use only the profile explicitly created in the current browser session. They no longer automatically select the newest local student record. This reduces accidental exposure on a shared computer, but it is **not authentication or multi-user security**.
- **Evidence-link validation:** optional progress links accept blank values or complete HTTP/HTTPS URLs only. External links are not verified by the application.
- **Explainable career fit:** each recommendation includes a component breakdown (skills, interests, and optional work-style/career-goal inputs) with effective weights and contribution points. The existing scoring formula was retained.
- **Profile context:** Python level, favourite subjects, and described project experience now guide learning suggestions. These context fields do **not** alter the numeric career-fit score. Descriptions remain self-reported, not independently verified.
- **Saved-assessment recovery:** the Results page can reload the latest assessment for the active student ID in the current browser session. It does not search for or select another student automatically.
- **Data connection handling:** SQLite connections are closed reliably after each operation. No schema migration or database reset is performed by this update.
- **Market/employer caveats:** the Market Explorer displays its snapshot date prominently; the employer comparison states that the current sample consists of two dated examples from one employer.
- **Learning evidence:** My Progress states that task completion is self-reported and does not independently verify mastery. Daily mission completion remains session-only and is labelled as such.

## Data and privacy for this release

This source archive does not include `data/career_compass.db`. On first launch, the application creates a local database if one does not exist. The ZIP intentionally excludes local databases and personal learner records. Back up any existing local database on your computer before copying updated source files into your working folder. Do not migrate or replace a database without a separate tested backup.

The local record ID in Streamlit session state is a navigation convenience, not a password. Do not use this prototype for multiple students on a shared public computer with real personal data. Production use would require authentication, access control, reviewed privacy practices, secure hosting, backups, and deletion workflows.

## Verification status

- Automated tests: **21 passed** in the release-hardening working copy.
- Python syntax compilation: passed for application, page, and test modules.
- Visual browser testing and clean Windows extraction/launch: **not yet verified** in this build environment. Streamlit was not installed in the build environment, so do not describe the UI as fully visually tested.
- Market-source URLs and current posting status still require a manual final review before public presentation.
