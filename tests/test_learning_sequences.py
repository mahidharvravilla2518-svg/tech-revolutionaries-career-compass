import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LearningSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.market = json.loads((ROOT / "market_signals.json").read_text(encoding="utf-8"))
        cls.sequence_data = json.loads((ROOT / "learning_sequences.json").read_text(encoding="utf-8"))

    def test_every_tracked_skill_has_a_recommended_path(self):
        tracked = {skill["name"] for skill in self.market["skills"]}
        self.assertEqual(tracked, set(self.sequence_data["pathways"]))
        self.assertEqual(tracked, set(self.sequence_data["guidance"]))

    def test_every_path_uses_known_skills_and_ends_at_its_target(self):
        known = {skill["name"] for skill in self.market["skills"]}
        for target, path in self.sequence_data["pathways"].items():
            steps = path["steps"]
            self.assertTrue(steps, f"{target} has no learning steps")
            self.assertEqual(target, steps[-1], f"{target} must be the final required step")
            self.assertEqual(len(steps), len(set(steps)), f"{target} repeats a required step")
            self.assertTrue(set(steps).issubset(known), f"{target} includes an unknown skill")
            self.assertTrue(set(path.get("optional_steps", [])).issubset(known))
            self.assertTrue(set(path.get("next_after", [])).issubset(known))

    def test_every_guidance_entry_has_actionable_focus_and_readiness(self):
        for skill, guidance in self.sequence_data["guidance"].items():
            for field in ("purpose", "focus", "ready_when"):
                self.assertTrue(guidance.get(field), f"{skill} is missing {field}")

    def test_foundation_first_for_major_ai_data_paths(self):
        foundation = "Programming Fundamentals"
        for target in ("SQL and Database Skills", "Data Analysis and Storytelling", "AI and Machine Learning", "Data Engineering and Pipelines", "LLMs and Generative AI", "Green and Energy Data"):
            self.assertEqual(self.sequence_data["pathways"][target]["steps"][0], foundation, target)


if __name__ == "__main__":
    unittest.main()
