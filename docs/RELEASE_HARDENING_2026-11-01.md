# Career Compass 3.0 — Release-hardening log (1 November 2026)

## Baseline and approach

This update was made from the supplied `CareerCompass3_Sequence_Update.zip` in a separate working copy. The archive contained source files and tests but **did not contain `data/career_compass.db`**. No user database was copied, reset, migrated, or included in the release archive. The user's pre-existing local folder/database cannot be modified from this working copy; back it up locally before replacing files there.

The approach follows the supplied review: release hardening first, no feature expansion that introduces unverified data or deployment risk.

## Implemented changes

### 1. Database connection safety
- Replaced raw-connection usage with a context-managed SQLite connection.
- Commits on success, rolls back on failure, and closes in a `finally` block.
- Existing tables are created with `IF NOT EXISTS`; no data reset or migration is included.

### 2. Local profile selection and privacy guard
- Removed automatic newest-student selection from My Progress.
- Removed automatic newest-student selection from Learning Studio.
- Pages now require a profile ID created in the active browser session.
- Removed the recent local student-record listing from My Progress.
- UI clarifies the prototype has no authentication or secure multi-user record isolation.

This reduces accidental display of another local record but is not a substitute for login/access control.

### 3. Evidence URL validation
- Added URL validation for optional progress evidence links.
- Blank links are allowed. Nonblank links must be complete HTTP/HTTPS URLs.
- Whitespace/control characters, credentials embedded in URLs, malformed ports, other schemes, and overlong links are rejected.
- UI says external links are not verified by the application.

### 4. Recommendation transparency
- Added a component breakdown for Skills, Interests, and any supplied optional Work Style/Career Goal components.
- The breakdown displays overlap percentage, effective weight, and contribution points.
- Effective displayed weights are normalised to 100%.
- The underlying fit calculation/weights were not changed.
- Empty/low-information profiles are explicitly described as provisional.

### 5. Profile-context guidance
- Python level, favourite subjects, and described project experience now shape guidance text.
- These fields do not change the numerical fit score.
- Project descriptions are not labelled as independently verified evidence.

### 6. Assessment reload
- Added a Results-page action to reload the latest saved assessment for the active session's student ID.
- It does not search for or select another student's record automatically.
- Limitation: it cannot recover a student ID after the browser session has fully reset.

### 7. Market and learning honesty cues
- Market Explorer now shows the research snapshot date prominently and describes scores as qualitative, not live vacancies.
- Job Requirements and Results pages call out the two-posting/one-employer sample limitation.
- My Progress explains that task completion and evidence links are learner-reported and do not independently verify mastery.
- Learning Studio labels daily mission completion session-only and self-reported.

## Automated verification

Command run from the project root:

```powershell
python -m py_compile app.py engine.py ai_helper.py database.py ui_theme.py pages/*.py tests/*.py
python -m unittest discover -s tests -v
```

Result: **21 tests passed**. The suite uses a temporary SQLite DB in its database tests. Additional test coverage includes empty-profile handling, score-weight normalisation, profile-context guidance without changing score, evidence URL validation, exact-student assessment retrieval, and fictional demo profiles without database writes.

## Not completed / still requires target-machine verification

- Streamlit was not installed in the build environment; no full browser visual audit was performed.
- Clean Windows extraction and `run_app.bat` launch have not been verified from this build environment.
- Market/employer source links and current posting status have not been manually re-opened in this update.
- Daily mission state remains session-only.
- No authentication, multi-user isolation, or cloud sync was added.
- No evidence taxonomy with verified proof states was added.
- No measured job-posting sample, live scraping, vacancy count, AI grading, PDF/CSV export, or demo dashboard was added.

## Recommended next steps on the user's Windows machine

1. Back up the existing `data/career_compass.db` and preserve the old project folder.
2. Extract the release ZIP into a new folder first; do not overwrite the live project.
3. Run the provided tests using the user's configured Python interpreter.
4. Launch with `run_app.bat` and visually test all pages.
5. Walk through profile → results → employer comparison → Market Explorer → Learning Studio → progress update.
6. Manually re-open source links and check posting status/date.
7. Only after successful checks, decide whether to replace the working folder; do not migrate databases without a separate tested procedure.
