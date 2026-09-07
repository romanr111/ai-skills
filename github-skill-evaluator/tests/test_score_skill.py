#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("score_skill", ROOT / "scripts" / "score_skill.py")
score_skill = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(score_skill)


class ScoreSkillTests(unittest.TestCase):
    def base_scores(self, value=8):
        return {key: value for key in score_skill.WEIGHTS}

    def test_weights_total_100(self):
        self.assertEqual(sum(score_skill.WEIGHTS.values()), 100)

    def test_uniform_eight_scores_to_80(self):
        result = score_skill.calculate({"scores": self.base_scores(8)})
        self.assertEqual(result["score"], 80)
        self.assertEqual(result["tier"], "A")

    def test_community_popularity_has_low_effect(self):
        low = self.base_scores(7)
        high = dict(low)
        low["community_evidence"] = 0
        high["community_evidence"] = 10
        delta = score_skill.calculate({"scores": high})["score_exact"] - score_skill.calculate({"scores": low})["score_exact"]
        self.assertAlmostEqual(delta, 1.0, places=2)

    def test_safety_cap_overrides_arithmetic(self):
        result = score_skill.calculate({"scores": self.base_scores(10), "caps": ["D"]})
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["base_tier"], "S")
        self.assertEqual(result["tier"], "D")

    def test_missing_dimension_is_error(self):
        scores = self.base_scores(8)
        del scores["workflow_design"]
        with self.assertRaises(ValueError):
            score_skill.calculate({"scores": scores})


if __name__ == "__main__":
    unittest.main()
