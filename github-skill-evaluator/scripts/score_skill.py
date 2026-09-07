#!/usr/bin/env python3
"""Validate evidence-bound evaluator judgments and compute a secondary score.

The model judges. This script only enforces judgment form, evidence binding,
abstention, probe gating, coverage, tier caps, and arithmetic.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RUBRIC_VERSION = "2026-09-v2"

WEIGHTS = {
    "activation_scope": 10,
    "instruction_workflow": 13,
    "domain_expertise": 12,
    "verification": 12,
    "capability_uplift": 15,
    "evidence_effectiveness": 10,
    "safety": 10,
    "reusability_composability": 8,
    "context_efficiency": 5,
    "maintainability_docs": 5,
}

BAND_VALUES = {
    "absent": 0.00,
    "weak": 0.25,
    "adequate": 0.50,
    "strong": 0.75,
    "exceptional": 1.00,
}
ABSTAIN = "insufficient_evidence"

TIER_FLOORS = [(90, "S"), (80, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "F")]
TIER_ORDER = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
CONFIDENCE_ORDER = {"Low": 0, "Medium": 1, "High": 2}
LINE_RANGE_RE = re.compile(r"^\d+(?:-\d+)?$")


def raw_tier(score: float) -> str:
    for floor, tier in TIER_FLOORS:
        if score >= floor:
            return tier
    return "F"


def apply_caps(tier: str, caps: list[str]) -> str:
    result = tier
    for cap in caps:
        cap = cap.upper()
        if cap not in TIER_ORDER:
            raise ValueError(f"Unknown cap: {cap}")
        if TIER_ORDER[result] > TIER_ORDER[cap]:
            result = cap
    return result


def coverage_confidence_cap(coverage: float) -> str:
    if coverage < 0.70:
        return "Low"
    if coverage < 0.85:
        return "Medium"
    return "High"


def cap_confidence(requested: str | None, cap: str) -> str:
    if requested is None:
        return cap
    if requested not in CONFIDENCE_ORDER:
        raise ValueError("confidence must be High, Medium, or Low")
    return requested if CONFIDENCE_ORDER[requested] <= CONFIDENCE_ORDER[cap] else cap


def _resolve_evidence_path(root: Path, rel: str) -> Path:
    if not rel or Path(rel).is_absolute():
        raise ValueError(f"Evidence path must be a non-empty relative path: {rel!r}")
    candidate = (root / rel).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Evidence path escapes inspected_root: {rel}") from exc
    if not candidate.is_file():
        raise ValueError(f"Evidence path does not exist: {rel}")
    return candidate


def _validate_evidence_item(root: Path, dimension: str, item: dict) -> None:
    if not isinstance(item, dict):
        raise ValueError(f"{dimension}: each evidence item must be an object")
    path = item.get("path")
    if not isinstance(path, str):
        raise ValueError(f"{dimension}: evidence.path is required")
    evidence_file = _resolve_evidence_path(root, path)

    quote = item.get("quote")
    lines = item.get("lines")
    observation = item.get("observation")
    if not any(isinstance(v, str) and v.strip() for v in (quote, lines, observation)):
        raise ValueError(f"{dimension}: evidence needs quote, lines, or observation")

    text = evidence_file.read_text(encoding="utf-8", errors="replace")
    if isinstance(quote, str) and quote.strip() and quote not in text:
        raise ValueError(f"{dimension}: evidence quote not found in {path}")
    if isinstance(lines, str) and lines.strip():
        if not LINE_RANGE_RE.fullmatch(lines.strip()):
            raise ValueError(f"{dimension}: invalid line range {lines!r}")
        parts = [int(x) for x in lines.split("-")]
        start, end = (parts[0], parts[-1])
        line_count = max(1, len(text.splitlines()))
        if start < 1 or end < start or end > line_count:
            raise ValueError(f"{dimension}: line range {lines} outside {path} ({line_count} lines)")


def _resolve_probe_artifact(root: Path, rel: str, label: str) -> Path:
    if not isinstance(rel, str) or not rel.strip() or Path(rel).is_absolute():
        raise ValueError(f"uplift_probe.{label} must be a non-empty relative path")
    candidate = (root / rel).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"uplift_probe.{label} escapes probe_root: {rel}") from exc
    if not candidate.exists():
        raise ValueError(f"uplift_probe.{label} does not exist: {rel}")
    return candidate


def _validate_probe(payload: dict, uplift_band: str) -> str:
    probe = payload.get("uplift_probe")
    probe_required = uplift_band in {"strong", "exceptional"}
    if not isinstance(probe, dict):
        if probe_required:
            raise ValueError("capability_uplift strong/exceptional requires uplift_probe")
        return "Inferred"

    probe_root_value = probe.get("probe_root")
    if not isinstance(probe_root_value, str) or not probe_root_value.strip():
        raise ValueError("uplift_probe.probe_root is required when a probe is supplied")
    probe_root = Path(probe_root_value).resolve()
    if not probe_root.is_dir():
        raise ValueError(f"uplift_probe.probe_root is not a directory: {probe_root}")

    for key in ("task", "judge_verdict", "execution_model"):
        if not isinstance(probe.get(key), str) or not probe[key].strip():
            raise ValueError(f"uplift_probe.{key} is required")

    with_output = _resolve_probe_artifact(probe_root, probe.get("with_skill_output"), "with_skill_output")
    baseline_output = _resolve_probe_artifact(probe_root, probe.get("baseline_output"), "baseline_output")
    if with_output == baseline_output:
        raise ValueError("uplift_probe with-skill and baseline outputs must be different artifacts")

    if probe.get("same_model_environment") is not True:
        raise ValueError("uplift_probe.same_model_environment must be true")
    if probe.get("judged_blind") is not True:
        raise ValueError("uplift_probe.judged_blind must be true")

    runs = probe.get("runs")
    if not isinstance(runs, int) or runs < 1:
        raise ValueError("uplift_probe.runs must be an integer >= 1")
    if uplift_band == "exceptional" and runs < 3:
        raise ValueError("exceptional capability_uplift requires at least 3 probe runs")
    return "Probed"


def _validate_counter_case(payload: dict, scored_keys: set[str]) -> dict:
    counter = payload.get("counter_case")
    if not isinstance(counter, dict):
        raise ValueError("counter_case is required")
    for key in ("argument", "what_would_change_my_mind"):
        if not isinstance(counter.get(key), str) or len(counter[key].strip()) < 20:
            raise ValueError(f"counter_case.{key} must be a substantive non-empty statement")
    at_risk = counter.get("dimensions_at_risk")
    if not isinstance(at_risk, list) or not at_risk:
        raise ValueError("counter_case.dimensions_at_risk must be a non-empty list")
    unknown = sorted(set(at_risk) - scored_keys)
    if unknown:
        raise ValueError(f"counter_case references unscored/unknown dimensions: {', '.join(unknown)}")
    return counter


def calculate(payload: dict) -> dict:
    if sum(WEIGHTS.values()) != 100:
        raise RuntimeError("Rubric weights must total 100")

    judge_model = payload.get("judge_model")
    if not isinstance(judge_model, str) or not judge_model.strip():
        raise ValueError("judge_model is required; scores are model-relative")

    root_value = payload.get("inspected_root")
    if not isinstance(root_value, str) or not root_value.strip():
        raise ValueError("inspected_root is required for evidence-path validation")
    root = Path(root_value).resolve()
    if not root.is_dir():
        raise ValueError(f"inspected_root is not a directory: {root}")

    dimensions = payload.get("dimensions")
    if not isinstance(dimensions, dict):
        raise ValueError("dimensions must be an object")
    missing = sorted(set(WEIGHTS) - set(dimensions))
    extra = sorted(set(dimensions) - set(WEIGHTS))
    if missing:
        raise ValueError(f"Missing dimensions: {', '.join(missing)}")
    if extra:
        raise ValueError(f"Unknown dimensions: {', '.join(extra)}")

    answered_weight = 0
    weighted_value = 0.0
    scored_keys: set[str] = set()
    abstained: list[str] = []

    for key, weight in WEIGHTS.items():
        record = dimensions[key]
        if not isinstance(record, dict):
            raise ValueError(f"{key}: dimension record must be an object")
        band = record.get("band")
        if band == ABSTAIN:
            abstained.append(key)
            evidence = record.get("evidence", [])
            if evidence not in ([], None):
                if not isinstance(evidence, list):
                    raise ValueError(f"{key}: evidence must be a list")
                for item in evidence:
                    _validate_evidence_item(root, key, item)
            reasoning = record.get("reasoning")
            if not isinstance(reasoning, str) or not reasoning.strip():
                raise ValueError(f"{key}: abstention requires reasoning")
            continue
        if band not in BAND_VALUES:
            allowed = ", ".join([*BAND_VALUES, ABSTAIN])
            raise ValueError(f"{key}: illegal band {band!r}; allowed: {allowed}")

        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError(f"{key}: scored dimension requires non-empty evidence")
        for item in evidence:
            _validate_evidence_item(root, key, item)

        reasoning = record.get("reasoning")
        if not isinstance(reasoning, str) or not reasoning.strip():
            raise ValueError(f"{key}: reasoning is required")

        answered_weight += weight
        weighted_value += BAND_VALUES[band] * weight
        scored_keys.add(key)

    if answered_weight == 0:
        raise ValueError("All dimensions abstained; no score can be calculated")

    uplift_band = dimensions["capability_uplift"].get("band")
    uplift_evidence = "Insufficient evidence" if uplift_band == ABSTAIN else _validate_probe(payload, uplift_band)
    counter = _validate_counter_case(payload, scored_keys)

    coverage = answered_weight / 100.0
    score_exact = weighted_value / answered_weight * 100.0
    score = int(round(score_exact))
    base_tier = raw_tier(score_exact)
    final_tier = apply_caps(base_tier, payload.get("caps", []))
    coverage_cap = coverage_confidence_cap(coverage)
    confidence = cap_confidence(payload.get("confidence"), coverage_cap)

    return {
        "rubric_version": RUBRIC_VERSION,
        "judge_model": judge_model,
        "score": score,
        "score_exact": round(score_exact, 2),
        "score_role": "secondary_summary_not_ranking_truth",
        "coverage": round(coverage, 3),
        "answered_weight": answered_weight,
        "abstained_dimensions": abstained,
        "coverage_confidence_cap": coverage_cap,
        "confidence": confidence,
        "base_tier": base_tier,
        "tier": final_tier,
        "caps": payload.get("caps", []),
        "capability_uplift_evidence": uplift_evidence,
        "counter_case": counter,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} evaluation.json", file=sys.stderr)
        return 2
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = calculate(payload)
    except (OSError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
