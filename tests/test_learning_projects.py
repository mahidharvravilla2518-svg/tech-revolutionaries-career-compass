import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LearningProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.market = json.loads((ROOT / "market_signals.json").read_text(encoding="utf-8"))
        cls.data = json.loads((ROOT / "learning_projects.json").read_text(encoding="utf-8"))

    def test_every_market_track_has_a_complete_project_brief(self):
        track_names = {skill["name"] for skill in self.market["skills"]}
        projects = {project["skill"]: project for project in self.data["projects"]}
        self.assertEqual(track_names, set(projects))
        required_fields = ["title", "problem_user", "data_source_label", "task", "success_criteria", "deliverables", "limitations", "next_step", "book_resources"]
        for project in self.data["projects"]:
            for field in required_fields:
                self.assertIn(field, project, f"{project.get('skill')} is missing {field}")
                self.assertTrue(project[field], f"{project.get('skill')} has an empty {field}")
            self.assertGreaterEqual(len(project["success_criteria"]), 3)
            self.assertGreaterEqual(len(project["deliverables"]), 2)

    def test_included_datasets_exist_and_are_readable(self):
        for project in self.data["projects"]:
            rel_path = project.get("dataset_file")
            if not rel_path:
                continue
            path = (ROOT / rel_path).resolve()
            self.assertIn(ROOT.resolve(), path.parents, "Dataset path must stay inside the project")
            self.assertTrue(path.is_file(), f"Missing dataset: {rel_path}")
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertGreater(len(rows), 0, f"Dataset is empty: {rel_path}")

    def test_project_source_urls_are_http_links_when_present(self):
        for project in self.data["projects"]:
            url = project.get("data_source_url", "")
            if url:
                self.assertTrue(url.startswith("https://"), f"Expected HTTPS source URL: {url}")
            for resource in project.get("book_resources", []):
                self.assertTrue(resource["url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
