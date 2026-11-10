import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MarketDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "market_signals.json").read_text(encoding="utf-8"))
        cls.sources = {item["id"] for item in cls.data["sources"]}

    def test_skills_have_transparent_scores_and_project_ideas(self):
        self.assertGreaterEqual(len(self.data["skills"]), 8)
        for skill in self.data["skills"]:
            self.assertIn(skill["signal_score"], [1, 2, 3, 4, 5])
            self.assertTrue(skill["one_line"].strip())
            self.assertTrue(skill["project"].strip())

    def test_all_salary_sources_exist(self):
        for role in self.data["roles"]:
            self.assertIn(role["source_id"], self.sources)
            self.assertLessEqual(role["low_lpa"], role["high_lpa"])
            self.assertTrue(role["caveat"].strip())

    def test_skill_evidence_ids_exist(self):
        for skill in self.data["skills"]:
            for source_id in skill.get("evidence", []):
                self.assertIn(source_id, self.sources)

    def test_snapshot_discloses_non_live_method(self):
        self.assertIn("2026-10-27", self.data["meta"]["as_of"])
        self.assertIn("not a count", self.data["meta"]["method_note"])


if __name__ == "__main__":
    unittest.main()
