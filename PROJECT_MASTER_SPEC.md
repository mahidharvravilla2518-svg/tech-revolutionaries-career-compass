# Project master specification

The single source of truth for the Career Compass mission, features, evidence rules, learning design, UI guidelines, privacy, testing, and definition of done is `BUILD_PROMPT.md`.

## Current implementation snapshot

Implemented in this version: existing profile/career fit flow, job requirements and skill-gap page, SQLite progress tracking, searchable curated market-signal dataset, salary context with dated references, economic-shift notes, Learning Studio, structured project briefs, synthetic practice datasets, ordered prerequisite-aware learning routes with readiness checks, and tests.

Not implemented as a live service: real-time job-board scraping, live vacancy counts, cross-device user accounts/sync, scheduled push/email reminders, automatic ingestion of uploaded books, or production-grade multi-user deployment. The app must state these limits honestly.


## Release-hardening implementation snapshot (2026-11-01)

Implemented in the release-hardening copy:
- SQLite connection context manager commits/rolls back and always closes connections.
- My Progress and Learning Studio no longer auto-select the latest local student record; only the active browser-session profile is used.
- Evidence URLs are validated as blank or HTTP/HTTPS before progress updates are stored.
- Recommendation results expose score components and effective weights without changing the existing fit formula.
- Python level, favourite subjects, and described project experience add contextual guidance but do not change numeric fit scores.
- Results page can reload an assessment for the active session's student ID.
- Market snapshot date and employer sample limitations are made more prominent.
- UI states that task completion is self-reported and not independent verification.
- Automated tests cover blank profiles, score breakdown, context guidance, URL validation, explicit assessment retrieval, and fictional profiles without DB writes.

Still deferred/not verified:
- No authentication, student account isolation, or cross-device sync.
- Daily mission checkbox remains session-only.
- Saved-assessment reload requires an active student ID in the current browser session; it does not recover an ID after a full session reset.
- No new evidence-level taxonomy (course-only/project-backed/portfolio-linked) or employer verification workflow.
- No automated demo dashboard, CSV/PDF export, measured job-posting sample, live scraping, or AI grading.
- Visual browser audit, clean Windows extraction test, and manual source URL/status verification remain pending.
