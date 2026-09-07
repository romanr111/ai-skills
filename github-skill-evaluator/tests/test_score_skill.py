#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("score_skill", ROOT / "scripts" / "score_skill.py")
score_skill = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(score_skill)


class ScoreSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        (self.repo / "SKILL.md").write_text("line one\nline two evidence\nline three\n", encoding="utf-8")

        self.probe = Path(self.tmp.name) / "probe"
        self.probe.mkdir()
        (self.probe / "with.txt").write_text("with-skill result\n", encoding="utf-8")
        (self.probe / "baseline.txt").write_text("baseline result\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, band="strong"):
        return {
            "band": band,
            "evidence": [{"path": "SKILL.md", "lines": "1-2", "quote": "line two evidence"}],
            "reasoning": "Grounded judgment based on the inspected skill entry point.",
        }

    def payload(self, band="strong"):
        return {
            "judge_model": "test-model",
            "inspected_root": str(self.repo),
            "confidence": "High",
            "dimensions": {key: self.record(band) for key in score_skill.WEIGHTS},
            "uplift_probe": {
                "task": "Representative task",
                "probe_root": str(self.probe),
                "with_skill_output": "with.txt",
                "baseline_output": "baseline.txt",
                "execution_model": "test-execution-model",
                "same_model_environment": True,
                "judged_blind": True,
                "judge_verdict": "With-skill output materially improves the target behavior.",
                "runs": 1,
            },
            "counter_case": {
                "argument": "The observed improvement may reflect prompt ordering rather than durable capability.",
                "dimensions_at_risk": ["capability_uplift"],
                "what_would_change_my_mind": "A matched baseline that performs equally well across repeated representative tasks.",
            },
            "caps": [],
        }

    def test_weights_total_100(self):
        self.assertEqual(sum(score_skill.WEIGHTS.values()), 100)
        self.assertEqual(len(score_skill.WEIGHTS), 10)

    def test_uniform_strong_is_75(self):
        result = score_skill.calculate(self.payload("strong"))
        self.assertEqual(result["score"], 75)
        self.assertEqual(result["coverage"], 1.0)

    def test_abstention_renormalizes_and_reports_coverage(self):
        payload = self.payload("strong")
        payload["dimensions"]["maintainability_docs"] = {
            "band": "insufficient_evidence",
            "evidence": [],
            "reasoning": "Repository history was unavailable, so this dimension is not scored.",
        }
        result = score_skill.calculate(payload)
        self.assertEqual(result["score"], 75)
        self.assertEqual(result["answered_weight"], 95)

    def test_illegal_band_is_rejected(self):
        payload = self.payload()
        payload["dimensions"]["domain_expertise"]["band"] = "8.5"
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_missing_evidence_is_rejected(self):
        payload = self.payload()
        payload["dimensions"]["domain_expertise"]["evidence"] = []
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_bad_quote_is_rejected(self):
        payload = self.payload()
        payload["dimensions"]["domain_expertise"]["evidence"][0]["quote"] = "not in file"
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_strong_uplift_requires_probe(self):
        payload = self.payload()
        del payload["uplift_probe"]
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_adequate_uplift_without_probe_is_inferred(self):
        payload = self.payload()
        payload["dimensions"]["capability_uplift"] = self.record("adequate")
        del payload["uplift_probe"]
        self.assertEqual(score_skill.calculate(payload)["capability_uplift_evidence"], "Inferred")

    def test_exceptional_uplift_requires_repetition(self):
        payload = self.payload()
        payload["dimensions"]["capability_uplift"] = self.record("exceptional")
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)
        payload["uplift_probe"]["runs"] = 3
        self.assertEqual(score_skill.calculate(payload)["capability_uplift_evidence"], "Probed")

    def test_probe_artifacts_must_exist(self):
        payload = self.payload()
        payload["uplift_probe"]["with_skill_output"] = "missing.txt"
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_probe_requires_same_model_environment(self):
        payload = self.payload()
        payload["uplift_probe"]["same_model_environment"] = False
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_probe_outputs_must_be_distinct(self):
        payload = self.payload()
        payload["uplift_probe"]["baseline_output"] = "with.txt"
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_counter_case_is_required(self):
        payload = self.payload()
        del payload["counter_case"]
        with self.assertRaises(ValueError):
            score_skill.calculate(payload)

    def test_coverage_caps_confidence(self):
        payload = self.payload()
        for key in ["activation_scope", "instruction_workflow", "domain_expertise"]:
            payload["dimensions"][key] = {
                "band": "insufficient_evidence",
                "evidence": [],
                "reasoning": "Evidence unavailable for this test.",
            }
        result = score_skill.calculate(payload)
        self.assertLess(result["coverage"], 0.70)
        self.assertEqual(result["confidence"], "Low")

    def test_safety_cap_overrides_arithmetic(self):
        payload = self.payload("exceptional")
        payload["uplift_probe"]["runs"] = 3
        payload["caps"] = ["D"]
        result = score_skill.calculate(payload)
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["tier"], "D")


if __name__ == "__main__":
    unittest.main()
