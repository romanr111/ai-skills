#!/usr/bin/env python3
"""Validate the portable github-skill-evaluator package.

Checks the core Agent Skills constraints that can be validated locally, plus
package-specific scoring/eval invariants. This is intentionally dependency-free.
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
    "references/domain-overlays.md",
    "references/red-flags.md",
    "references/output-format.md",
    "references/installation.md",
    "scripts/score_skill.py",
    "evals/evals.json",
]


def parse_simple_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        return None, "Could not parse SKILL.md frontmatter"
    data: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            return None, f"Invalid frontmatter line: {raw!r}"
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip()
    return data, None


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    forbidden = [p for p in root.rglob("*") if p.name == "__pycache__" or p.suffix == ".pyc"]
    if forbidden:
        errors.append("Generated Python cache artifacts must not be packaged")

    skill = root / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        fm, fm_error = parse_simple_frontmatter(text)
        if fm_error:
            errors.append(fm_error)
        elif fm is not None:
            # Portable minimal core: keep only the two required standard fields.
            if set(fm) != {"name", "description"}:
                errors.append("Portable SKILL.md frontmatter must contain only name and description")

            name = fm.get("name", "")
            description = fm.get("description", "")
            if not (1 <= len(name) <= 64):
                errors.append("Skill name must be 1-64 characters")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                errors.append("Skill name must be lowercase kebab-case without consecutive/edge hyphens")
            if root.name != name:
                errors.append(f"Skill name {name!r} must match parent directory {root.name!r}")
            if not (1 <= len(description) <= 1024):
                errors.append("Skill description must be 1-1024 characters")
            if "<" in name or ">" in name or "<" in description or ">" in description:
                errors.append("Skill name/description must not contain XML-like angle brackets")

        if len(text.splitlines()) > 500:
            errors.append("SKILL.md exceeds 500 lines; use progressive disclosure")

        # Local relative markdown links from SKILL.md should resolve.
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (root / clean).exists():
                errors.append(f"Broken relative reference in SKILL.md: {target}")

    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.is_file():
        meta = openai_yaml.read_text(encoding="utf-8")
        m = re.search(r'^\s*short_description:\s*"([^"]+)"', meta, flags=re.M)
        if not m or not 25 <= len(m.group(1)) <= 64:
            errors.append("agents/openai.yaml short_description must be 25-64 characters")
        m = re.search(r'^\s*default_prompt:\s*"([^"]+)"', meta, flags=re.M)
        if not m or "$github-skill-evaluator" not in m.group(1):
            errors.append("agents/openai.yaml default_prompt must mention $github-skill-evaluator")

    score_path = root / "scripts/score_skill.py"
    score_text = score_path.read_text(encoding="utf-8") if score_path.is_file() else ""
    weights_match = re.search(r"WEIGHTS\s*=\s*\{(.*?)\n\}", score_text, flags=re.S)
    if not weights_match:
        errors.append("Could not locate WEIGHTS block in score_skill.py")
    else:
        weights = [int(x) for x in re.findall(r'^\s+"[a-z_]+":\s+(\d+),$', weights_match.group(1), flags=re.M)]
        if len(weights) != 18:
            errors.append(f"Expected 18 rubric weights, found {len(weights)}")
        if sum(weights) != 100:
            errors.append(f"Score weights total {sum(weights)}, expected 100")

    eval_path = root / "evals/evals.json"
    if eval_path.is_file():
        try:
            payload = json.loads(eval_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid evals/evals.json: {exc}")
        else:
            if payload.get("skill_name") != "github-skill-evaluator":
                errors.append("evals/evals.json skill_name must match the skill")
            evals = payload.get("evals")
            if not isinstance(evals, list) or len(evals) < 5:
                errors.append("evals/evals.json must contain at least 5 behavioral evals")
            else:
                ids = set()
                for case in evals:
                    if not isinstance(case, dict):
                        errors.append("Each eval case must be an object")
                        continue
                    case_id = case.get("id")
                    if not isinstance(case_id, int) or case_id in ids:
                        errors.append("Eval ids must be unique integers")
                    ids.add(case_id)
                    if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                        errors.append(f"Eval {case_id}: prompt is required")
                    if not isinstance(case.get("expected_output"), str) or not case["expected_output"].strip():
                        errors.append(f"Eval {case_id}: expected_output is required")
                    if not isinstance(case.get("files"), list):
                        errors.append(f"Eval {case_id}: files must be a list")
                    expectations = case.get("expectations")
                    if not isinstance(expectations, list) or not expectations:
                        errors.append(f"Eval {case_id}: expectations must be a non-empty list")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: Agent Skills structure, references, rubric, metadata, and eval schema validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
