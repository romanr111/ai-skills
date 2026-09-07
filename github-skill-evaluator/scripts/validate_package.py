#!/usr/bin/env python3
"""Validate the portable github-skill-evaluator package.

Checks portable Agent Skills structure plus evaluator-specific invariants.
This does not claim the behavioral evals have passed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "SKILL.md",
    "references/evaluation-rubric.md",
    "references/repository-inspection.md",
    "references/discovery.md",
    "references/claim-validation.md",
    "references/domain-overlays.md",
    "references/red-flags.md",
    "references/output-format.md",
    "references/installation.md",
    "scripts/score_skill.py",
    "scripts/repo_inventory.py",
    "tests/test_score_skill.py",
    "evals/evals.json",
    "evals/trigger-cases.json",
]

DIMENSION_KEYS = ["activation_scope", "instruction_workflow", "domain_expertise", "verification", "capability_uplift", "evidence_effectiveness", "safety", "reusability_composability", "context_efficiency", "maintainability_docs"]
BANDS = ["absent", "weak", "adequate", "strong", "exceptional"]


def parse_simple_frontmatter(text: str):
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not match: return None, "Could not parse SKILL.md frontmatter"
    data = {}
    for raw in match.group(1).splitlines():
        if not raw.strip(): continue
        if ":" not in raw: return None, f"Invalid frontmatter line: {raw!r}"
        key, value = raw.split(":", 1); data[key.strip()] = value.strip()
    return data, None


def validate(root: Path) -> list[str]:
    errors = []
    for rel in REQUIRED:
        if not (root / rel).is_file(): errors.append(f"Missing required file: {rel}")
    if any(p.name == "__pycache__" or p.suffix == ".pyc" for p in root.rglob("*")):
        errors.append("Generated Python cache artifacts must not be packaged")

    skill = root / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        fm, err = parse_simple_frontmatter(text)
        if err: errors.append(err)
        elif fm is not None:
            if set(fm) != {"name", "description"}: errors.append("Portable SKILL.md frontmatter must contain only name and description")
            name, description = fm.get("name", ""), fm.get("description", "")
            if not (1 <= len(name) <= 64): errors.append("Skill name must be 1-64 characters")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name): errors.append("Skill name must be lowercase kebab-case")
            if root.name != name: errors.append(f"Skill name {name!r} must match directory {root.name!r}")
            if not (1 <= len(description) <= 1024): errors.append("Skill description must be 1-1024 characters")
            if "<" in name or ">" in name or "<" in description or ">" in description: errors.append("Skill name/description must not contain XML-like angle brackets")
        if len(text.splitlines()) > 500: errors.append("SKILL.md exceeds 500 lines; use progressive disclosure")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"): continue
            clean = target.split("#", 1)[0]
            if clean and not (root / clean).exists(): errors.append(f"Broken relative reference in SKILL.md: {target}")

    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.is_file():
        meta = openai_yaml.read_text(encoding="utf-8")
        match = re.search(r'^\s*short_description:\s*"([^"]+)"', meta, flags=re.M)
        if not match or not 25 <= len(match.group(1)) <= 64: errors.append("agents/openai.yaml short_description must be 25-64 characters")
        match = re.search(r'^\s*default_prompt:\s*"([^"]+)"', meta, flags=re.M)
        if not match or "$github-skill-evaluator" not in match.group(1): errors.append("agents/openai.yaml default_prompt must mention $github-skill-evaluator")

    score_path = root / "scripts/score_skill.py"
    if score_path.is_file():
        score_text = score_path.read_text(encoding="utf-8")
        if 'RUBRIC_VERSION = "2026-09-v2"' not in score_text: errors.append("score_skill.py must stamp rubric version 2026-09-v2")
        match = re.search(r"WEIGHTS\s*=\s*\{(.*?)\n\}", score_text, flags=re.S)
        if not match: errors.append("Could not locate WEIGHTS block")
        else:
            pairs = re.findall(r'^\s+"([a-z_]+)":\s+(\d+),$', match.group(1), flags=re.M)
            keys, weights = [k for k,_ in pairs], [int(v) for _,v in pairs]
            if keys != DIMENSION_KEYS: errors.append(f"Expected 10 rubric keys in canonical order, found {keys}")
            if sum(weights) != 100: errors.append(f"Rubric weights total {sum(weights)}, expected 100")
        for band in BANDS:
            if f'"{band}"' not in score_text: errors.append(f"score_skill.py missing band {band}")
        if 'ABSTAIN = "insufficient_evidence"' not in score_text: errors.append("score_skill.py must support insufficient_evidence abstention")
        for probe_field in ("probe_root", "with_skill_output", "baseline_output", "execution_model", "same_model_environment", "judged_blind"):
            if probe_field not in score_text: errors.append(f"score_skill.py missing uplift probe field {probe_field}")

    rubric = root / "references/evaluation-rubric.md"
    if rubric.is_file():
        text = rubric.read_text(encoding="utf-8")
        if "**Rubric version:** `2026-09-v2`" not in text: errors.append("evaluation-rubric.md missing rubric version")
        sections = re.split(r"(?m)^### \d+\. ", text)[1:]
        if len(sections) != 10: errors.append(f"Expected 10 dimension anchor sections, found {len(sections)}")
        else:
            for index, section in enumerate(sections, start=1):
                for band in BANDS:
                    if f"`{band}`" not in section: errors.append(f"Dimension {index} missing anchor for {band}")

    eval_path = root / "evals/evals.json"
    if eval_path.is_file():
        try: payload = json.loads(eval_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: errors.append(f"Invalid evals/evals.json: {exc}")
        else:
            if payload.get("skill_name") != "github-skill-evaluator": errors.append("evals/evals.json skill_name mismatch")
            evals = payload.get("evals")
            if not isinstance(evals, list) or len(evals) < 8: errors.append("evals/evals.json must contain at least 8 behavioral cases")
            else:
                ids = set()
                for case in evals:
                    if not isinstance(case, dict): errors.append("Each eval case must be an object"); continue
                    cid = case.get("id")
                    if not isinstance(cid, int) or cid in ids: errors.append("Eval ids must be unique integers")
                    ids.add(cid)
                    if not isinstance(case.get("prompt"), str) or not case["prompt"].strip(): errors.append(f"Eval {cid}: prompt required")
                    if not isinstance(case.get("assertions"), list) or not case["assertions"]: errors.append(f"Eval {cid}: assertions must be non-empty")

    trigger_path = root / "evals/trigger-cases.json"
    if trigger_path.is_file():
        try: cases = json.loads(trigger_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: errors.append(f"Invalid trigger-cases.json: {exc}")
        else:
            if not isinstance(cases, list) or len(cases) < 16: errors.append("trigger-cases.json must contain at least 16 cases")
            else:
                positives = sum(c.get("should_trigger") is True for c in cases if isinstance(c, dict))
                negatives = sum(c.get("should_trigger") is False for c in cases if isinstance(c, dict))
                splits = {c.get("split") for c in cases if isinstance(c, dict)}
                if positives < 8 or negatives < 8: errors.append("Trigger eval needs at least 8 positive and 8 near-miss negative cases")
                if not {"train", "held_out"}.issubset(splits): errors.append("Trigger eval must include train and held_out splits")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        for error in errors: print(f"ERROR: {error}")
        return 1
    print("OK: structure, metadata, evidence-band rubric, scorer invariants, and eval schemas validated")
    return 0


if __name__ == "__main__": raise SystemExit(main())
