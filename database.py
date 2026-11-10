"""SQLite persistence for local college-demo use.

Connections are always closed after each operation. The database remains local;
this module does not provide authentication or multi-user security.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "career_compass.db"


@contextmanager
def connect():
    """Yield a configured SQLite connection and always close it."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            display_name TEXT,
            year_of_study TEXT,
            profile_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL,
            recommendations_json TEXT NOT NULL,
            action_plan_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS progress_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            assessment_id INTEGER REFERENCES assessments(id) ON DELETE SET NULL,
            task_title TEXT NOT NULL,
            task_detail TEXT,
            evidence_url TEXT,
            status TEXT NOT NULL DEFAULT 'Not started',
            due_week INTEGER DEFAULT 1,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS job_sources (
            job_id TEXT PRIMARY KEY,
            employer TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            source_url TEXT NOT NULL,
            checked_on TEXT NOT NULL,
            payload_json TEXT NOT NULL
        );
        """)


def save_assessment(profile, recommendations, action_plan):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as con:
        cur = con.execute(
            "INSERT INTO students(created_at, display_name, year_of_study, profile_json) VALUES(?,?,?,?)",
            (now, profile.get("display_name") or None,
             str(profile.get("year_label") or profile.get("year") or ""),
             json.dumps(profile, ensure_ascii=False)),
        )
        student_id = cur.lastrowid
        cur = con.execute(
            "INSERT INTO assessments(student_id, created_at, recommendations_json, action_plan_json) VALUES(?,?,?,?)",
            (student_id, now, json.dumps(recommendations, ensure_ascii=False),
             json.dumps(action_plan, ensure_ascii=False)),
        )
        assessment_id = cur.lastrowid
        for rec in recommendations[:3]:
            title = rec.get("starter_project") or f"Explore {rec.get('title', 'career')}"
            con.execute(
                "INSERT INTO progress_tasks(student_id, assessment_id, task_title, task_detail, due_week, updated_at) VALUES(?,?,?,?,?,?)",
                (student_id, assessment_id, title,
                 f"Starter project for {rec.get('title', 'career')}", 1, now),
            )
        return student_id, assessment_id


def get_tasks(student_id):
    with connect() as con:
        rows = con.execute(
            "SELECT * FROM progress_tasks WHERE student_id=? ORDER BY due_week, id",
            (student_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def add_progress_task(student_id, task_title, task_detail, assessment_id=None, due_week=1):
    """Add a learning challenge without duplicating its title for a student."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as con:
        existing = con.execute(
            "SELECT id FROM progress_tasks WHERE student_id=? AND task_title=? LIMIT 1",
            (student_id, task_title),
        ).fetchone()
        if existing:
            return existing["id"], False
        cur = con.execute(
            "INSERT INTO progress_tasks(student_id, assessment_id, task_title, task_detail, due_week, updated_at) VALUES(?,?,?,?,?,?)",
            (student_id, assessment_id, task_title, task_detail, due_week, now),
        )
        return cur.lastrowid, True


def update_task(task_id, status, evidence_url):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as con:
        con.execute(
            "UPDATE progress_tasks SET status=?, evidence_url=?, updated_at=? WHERE id=?",
            (status, evidence_url or None, now, task_id),
        )


def latest_assessment(student_id):
    """Return a student's most recent saved assessment; never chooses a student."""
    with connect() as con:
        row = con.execute(
            "SELECT s.id AS student_id, s.profile_json, a.id AS assessment_id, "
            "a.recommendations_json, a.action_plan_json, a.created_at "
            "FROM students s JOIN assessments a ON a.student_id=s.id "
            "WHERE s.id=? ORDER BY a.id DESC LIMIT 1",
            (student_id,),
        ).fetchone()
    if row is None:
        return None
    item = dict(row)
    item["profile"] = json.loads(item.pop("profile_json"))
    item["recommendations"] = json.loads(item.pop("recommendations_json"))
    item["action_plan"] = json.loads(item.pop("action_plan_json"))
    return item


def recent_students(limit=20):
    """Return local record metadata for explicit administrative/demo use only."""
    with connect() as con:
        rows = con.execute(
            "SELECT s.id, s.created_at, s.display_name, s.year_of_study, a.id AS assessment_id "
            "FROM students s LEFT JOIN assessments a ON a.student_id=s.id "
            "ORDER BY s.id DESC LIMIT ?", (limit,),
        ).fetchall()
        return [dict(row) for row in rows]


def add_job_sources(jobs):
    with connect() as con:
        for job in jobs:
            con.execute(
                "INSERT OR REPLACE INTO job_sources(job_id, employer, role, location, source_url, checked_on, payload_json) VALUES(?,?,?,?,?,?,?)",
                (job["job_id"], job["employer"], job["role"], job.get("location", ""),
                 job["source_url"], job["checked_on"], json.dumps(job, ensure_ascii=False)),
            )
