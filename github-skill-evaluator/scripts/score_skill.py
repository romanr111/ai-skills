#!/usr/bin/env python3
"""Compute the weighted intrinsic score for github-skill-evaluator rubric.

Input JSON example:
{
  "scores": {
    "problem_scope": 8,
    "instruction_quality": 9,
    ...
  },
  "caps": []
}

Optional caps: "C", "D", "F". The strictest cap wins.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WEIGHTS = {
    "problem_scope": 4,
    "instruction_quality": 7,
    "domain_expertise": 8,
    "workflow_design": 8,
    "verification": 9,
    "reusability": 8,
    "composability": 4,
    "context_efficiency": 4,
    "tool_usage": 3,
    "code_script_quality": 3,
    "evidence_effectiveness": 8,
    "maintainability": 5,
    "safety": 8,
    "capability_uplift": 9,
    "sophistication": 5,
    "documentation": 4,
    "repository_health": 2,
    "community_evidence": 1,
}

TIER_FLOORS = [(90, "S"), (80, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "F")]
TIER_ORDER = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}


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


def calculate(payload: dict) -> dict:
    scores = payload.get("scores", {})
    missing = sorted(set(WEIGHTS) - set(scores))
    extra = sorted(set(scores) - set(WEIGHTS))
    if missing:
        raise ValueError(f"Missing scores: {', '.join(missing)}")
    if extra:
        raise ValueError(f"Unknown scores: {', '.join(extra)}")

    for key, value in scores.items():
        if not isinstance(value, (int, float)) or not 0 <= value <= 10:
            raise ValueError(f"{key} must be numeric in [0, 10], got {value!r}")

    if sum(WEIGHTS.values()) != 100:
        raise RuntimeError("Rubric weights must total 100")

    weighted = sum((scores[key] / 10.0) * weight for key, weight in WEIGHTS.items())
    rounded = int(round(weighted))
    base_tier = raw_tier(weighted)
    final_tier = apply_caps(base_tier, payload.get("caps", []))

    return {
        "score": rounded,
        "score_exact": round(weighted, 2),
        "base_tier": base_tier,
        "tier": final_tier,
        "caps": payload.get("caps", []),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} scores.json", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = calculate(payload)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
