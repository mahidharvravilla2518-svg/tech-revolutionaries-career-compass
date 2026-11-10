import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import database
from engine import recommend_careers, job_skill_gap, validate_evidence_url


class CompassTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = database.DB_PATH
        database.DB_PATH = Path(self.temp_dir.name) / "test_career_compass.db"
        self.catalog = json.loads((ROOT / "career_catalog.json").read_text(encoding="utf-8"))
        self.jobs = json.loads((ROOT / "job_requirements.json").read_text(encoding="utf-8"))
        database.init_db()

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_recommendations_return_three_and_score(self):
        profile = {"year": 2, "skills": ["Python", "SQL", "statistics"], "interests": ["data analysis", "mathematics"], "preferred_work": "analyzing data", "weekly_hours": 5}
        results = recommend_careers(profile, self.catalog, 3)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(0 <= item["fit_score"] <= 100 for item in results))
        self.assertTrue(all("score_note" in item for item in results))

    def test_incomplete_profile_still_gets_provisional_options(self):
        results = recommend_careers({"skills": [], "interests": ["technology"], "preferred_work": ""}, self.catalog, 3)
        self.assertEqual(len(results), 3)
        self.assertTrue(all("fit_score" in item for item in results))

    def test_score_breakdown_is_transparent_and_weights_sum_to_100(self):
        profile = {"skills": ["Python"], "interests": ["data analysis"], "preferred_work": "analyzing data"}
        result = recommend_careers(profile, self.catalog, 1)[0]
        self.assertAlmostEqual(sum(item["effective_weight_pct"] for item in result["score_breakdown"]), 100.0, places=1)
        self.assertGreaterEqual(result["fit_score"], 0)
        self.assertLessEqual(result["fit_score"], 100)

    def test_empty_or_missing_profile_is_safe_and_provisional(self):
        results = recommend_careers(None, self.catalog, 3)
        self.assertEqual(len(results), 3)
        self.assertTrue(all("provisional" in item["score_note"].lower() for item in results))

    def test_profile_context_personalises_guidance_without_changing_score(self):
        base = {"skills": ["Python"], "interests": ["data analysis"]}
        contextual = {**base, "python_skill_level": "Beginner", "favorite_subjects": ["Statistics"], "project_experience": ["Built a CSV dashboard"]}
        base_result = recommend_careers(base, self.catalog, 1)[0]
        contextual_result = recommend_careers(contextual, self.catalog, 1)[0]
        self.assertEqual(base_result["fit_score"], contextual_result["fit_score"])
        self.assertTrue(any("Statistics" in line for line in contextual_result["guidance"]))
        self.assertTrue(any("prior practical work" in line for line in contextual_result["guidance"]))

    def test_evidence_url_validation(self):
        self.assertEqual(validate_evidence_url(""), (True, ""))
        self.assertTrue(validate_evidence_url("https://github.com/example/repo")[0])
        self.assertTrue(validate_evidence_url("http://localhost:8501")[0])
        for value in ("javascript:alert(1)", "file:///C:/secret.txt", "example.com", "https://example.com/a b", "https://user:pass@example.com"):
            self.assertFalse(validate_evidence_url(value)[0], value)

    def test_fictional_demo_profiles_run_without_database_writes(self):
        profiles = json.loads((ROOT / "test_profiles.json").read_text(encoding="utf-8"))
        with database.connect() as con:
            before = con.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        for demo in profiles:
            profile = {
                "year": demo.get("year_of_study"),
                "skills": demo.get("skills", []),
                "interests": demo.get("interests", []),
                "favorite_subjects": demo.get("favorite_subjects", []),
                "python_skill_level": demo.get("python_skill_level", "Not assessed"),
                "project_experience": demo.get("project_experience", []),
                "target_career": demo.get("career_goal"),
            }
            self.assertTrue(recommend_careers(profile, self.catalog, 3))
        with database.connect() as con:
            after = con.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        self.assertEqual(before, after)

    def test_latest_assessment_loads_only_requested_student(self):
        profile = {"display_name": "TEST ONLY", "year": 2, "skills": ["SQL"], "interests": []}
        recs = recommend_careers(profile, self.catalog, 1)
        student_id, assessment_id = database.save_assessment(profile, recs, {"mode": "fallback", "thirty_day_plan": []})
        saved = database.latest_assessment(student_id)
        self.assertEqual(saved["student_id"], student_id)
        self.assertEqual(saved["assessment_id"], assessment_id)
        self.assertEqual(saved["profile"]["display_name"], "TEST ONLY")
        self.assertIsNone(database.latest_assessment(student_id + 9999))

    def test_job_gap_marks_unreported_not_absent(self):
        gap = job_skill_gap({"skills": ["SQL", "Python"]}, self.jobs[0])
        self.assertIn("sql", gap["matched"])
        self.assertIn("not_reported_or_unassessed", gap)

    def test_database_persists_task_and_does_not_duplicate_learning_project(self):
        profile = {"display_name": "TEST ONLY", "year": 2, "year_label": "2nd year", "skills": ["Python"], "interests": [], "weekly_hours": 2}
        recommendations = recommend_careers(profile, self.catalog, 1)
        student_id, assessment_id = database.save_assessment(profile, recommendations, {"mode": "fallback", "thirty_day_plan": []})
        tasks = database.get_tasks(student_id)
        self.assertGreaterEqual(len(tasks), 1)
        database.update_task(tasks[0]["id"], "In progress", "https://example.com/demo")
        self.assertEqual(database.get_tasks(student_id)[0]["status"], "In progress")

        task_id, created = database.add_progress_task(student_id, "Test learning project", "Project detail", assessment_id=assessment_id)
        self.assertTrue(created)
        duplicate_id, duplicate_created = database.add_progress_task(student_id, "Test learning project", "Project detail", assessment_id=assessment_id)
        self.assertEqual(task_id, duplicate_id)
        self.assertFalse(duplicate_created)


if __name__ == "__main__":
    unittest.main()
