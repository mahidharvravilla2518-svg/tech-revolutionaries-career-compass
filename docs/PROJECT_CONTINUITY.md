# Project continuity and safe upgrade notes

## What this version includes

This new project folder builds on the latest available Career Compass 2.0 project archive and its refreshed UI. It keeps the original profile assessment, career-fit engine, optional AI/fallback action plan, job-requirement comparison, SQLite progress features, and test profiles. It adds:

- a searchable, source-linked Market Explorer;
- a curated market-signal and salary-reference dataset;
- economic-shift interpretation for students;
- a project-first Learning Studio with daily in-app missions, structured challenge briefs, downloadable synthetic practice datasets, and an action to add a challenge to the local progress tracker;
- a reusable `BUILD_PROMPT.md` for future upgrades.

## What this archive cannot include

The live `data/career_compass.db` file from the user's laptop was not present in the available archive, so this package does not contain old local student records. The original folder on the user's computer should remain untouched. When this new folder is first run, it will create its own local database.

If there are important demo records in an older folder, keep that folder untouched and back up its database separately. Do not copy or migrate an older database into this version without checking schema compatibility and making a tested backup. This project creates its own local database if one is absent; it does not need a database file in the release ZIP.

## Research truth labels

`market_signals.json` is a dated research snapshot (2026-10-27), not live market data. The 1–5 signal score is a qualitative synthesis from cited reports, not a job-posting count or employment probability. Salary information is role-based, not a guaranteed amount paid for acquiring a skill. Conversions to monthly/weekly/hourly equivalents are arithmetic from annual gross figures; they are not in-hand pay or quoted hourly contract rates.

The learning CSVs are synthetic practice data; they are not real-world business measurements. Before a public presentation, reopen the linked sources and state that market claims are from the dated source, not a live scrape. To make a measured “current demand” graph later, collect a repeatable sample of public job listings across employers and locations, store the collection date, deduplicate listings, split by experience level, and show the sample size.

## Privacy and deployment

This project uses local SQLite and is suitable as a classroom prototype. Do not expose it publicly with real student data as-is. A public version needs reviewed hosting, privacy rules, authentication decisions, database durability, and error handling.


## Learning project brief format

`learning_projects.json` has one challenge per tracked market skill. Every challenge states its intended user/problem, data-source context, task, success criteria, deliverables, limitations, next step, and relevant reading links. The included CSV datasets are explicitly synthetic practice files. The Learning Studio can add a project to the current local profile's progress list; the app remains a single-user local prototype and is not safe for public multi-user use.


## 2026-11-01 release-hardening update

The supplied ZIP is a source-only package and does not contain the user's local `data/career_compass.db`. The release copy keeps the database out of the ZIP. Any existing database on the user's computer remains untouched by preparing this archive; back it up before manually replacing source files in an existing folder. No reset, schema migration, or database replacement is part of this update.

### Implemented in the release-hardening copy
- Database access now uses a context manager with commit/rollback and guaranteed connection closure.
- My Progress and Learning Studio no longer auto-select the latest local student record. A page requires an active profile in the current browser session.
- Optional evidence links are restricted to valid HTTP/HTTPS URL forms; blank is allowed.
- The Results page can reload the latest assessment for the active session's student ID.
- Career fit breakdown is visible by component, with effective weights normalised to 100%. The scoring formula itself is unchanged.
- Python level, favourite subjects and described project experience influence guidance only, not the fit score.
- UI labels profile inputs as self-reported and task completion as unverified.
- Market snapshot date and employer sample limitation are more visible.
- Five additional automated test cases were added; total test suite is 21 tests.

### Still a local prototype
The session student ID is not authentication. The changes reduce accidental auto-selection but do not create secure student account boundaries. Public or multi-user use still requires authentication/access-control decisions, reviewed privacy controls, secure hosting, backups and data-deletion workflows.

Daily mission completion remains session-only. A saved-assessment reload works only when the active student ID remains in Streamlit session state. It cannot identify a student after a full session reset, and intentionally does not guess based on the newest database row.

### Verification status
The release-hardening working copy passed 21 automated tests and Python syntax compilation. Browser-based visual inspection, clean Windows extraction/launch, and manual current-status checks of external market/employer links remain to be completed.
