# GitHub Skill Discovery Protocol

Use this protocol when the user asks to **find**, **discover**, **recommend**, or **rank** open-source Agent Skills and has not already supplied a complete candidate set.

## Goal

Build a decision-relevant candidate pool without letting popularity, search ranking, or a single vocabulary choice determine the result.

## 1. Translate the use case into search concepts

Extract:
- domain: e.g. frontend design, architecture, visual QA, testing, research;
- job-to-be-done: e.g. create, review, verify, migrate, benchmark;
- agent ecosystem terms: `Agent Skill`, `Claude Code skill`, `Codex skill`, `SKILL.md`;
- domain synonyms and adjacent terminology;
- hard constraints: license, model/tool compatibility, language, OS, offline use, MCP/browser requirements.

Generate several query families rather than one query. Example for visual QA:
- `visual QA agent skill`
- `visual regression Claude Code skill`
- `screenshot comparison SKILL.md`
- `frontend verification Codex skill`
- `pixel comparison agent skill`

Use both repository search and code/file search when available. Curated lists or “awesome” repositories may seed candidates, but never count as quality evidence.

## 2. Build a broad candidate pool

Aim for roughly **8–20 plausible candidates** when the ecosystem is large enough. Do not mechanically take the first search page.

Intentionally diversify the pool across:
- exact use-case matches;
- adjacent but potentially stronger approaches;
- established and low-popularity repositories;
- standalone skills and skill collections where the target unit can be isolated.

Search ranking and star count are discovery signals only.

## 3. Apply eligibility gates before deep evaluation

A candidate is eligible when it has enough inspectable material to determine what the skill actually does.

Check:
- an identifiable skill entry point such as `SKILL.md` or equivalent;
- repository/source availability;
- compatibility with the requested agent environment, or a feasible adaptation path;
- license/reuse status;
- no immediately disqualifying malicious or deceptive behavior.

### Open-source requirement

A public GitHub repository is not automatically open source.

When the user explicitly requests **open-source/reusable** skills:
- prefer a clear license permitting reuse/modification/distribution;
- classify a public repository with no clear license as `source-visible / reuse rights unclear`;
- do not present unclear-license candidates as fully reusable open-source recommendations without the caveat;
- exclude them from the top reusable recommendation when similarly capable clearly licensed alternatives exist.

## 4. Deduplicate and identify provenance

Before shortlisting:
- collapse forks, mirrors, copied bundles, and renamed copies where provenance is clear;
- prefer the upstream/original implementation unless a fork materially improves it;
- treat wrappers around the same underlying skill as one capability family unless their behavior differs materially;
- flag uncertain copied provenance.

Do not let the same underlying skill occupy multiple ranking slots.

## 5. Shortlist by semantic fit, not popularity

Reduce to roughly **3–8 candidates** for deep inspection using:
- direct problem match;
- unique claimed capability;
- apparent executability;
- compatibility and integration cost;
- presence of inspectable implementation/evidence;
- diversity of approach.

Do **not** shortlist primarily by stars, forks, author reputation, or README polish.

If the user asks for the “best” skills, include at least one credible lower-popularity candidate when available so the comparison can detect hidden gems.

## 6. Search saturation / stop condition

Stop discovery when:
- multiple query families return mostly the same candidates;
- new candidates are clearly weaker, duplicated, ineligible, or off-target;
- the shortlist contains enough distinct approaches to make the decision;
- further search is unlikely to change the top recommendation.

Continue searching when:
- only one vocabulary family was tried;
- the initial results are dominated by aggregators;
- all candidates are popularity-heavy but weakly evidenced;
- the use case has important synonyms not yet searched;
- the top candidates are near-tied and another approach could change the decision.

## 7. Freshness

Freshness matters when the skill depends on fast-changing APIs, agent formats, frameworks, security guidance, or model/tool behavior. In stable domains, do not equate newer with better.

Record material version/date assumptions when compatibility could change the result.

## Discovery output

When discovery itself is material, briefly report:
- search concepts used;
- number of plausible candidates considered;
- eligibility exclusions that matter;
- the deep-evaluation shortlist.

Do not dump every search result unless the user asks for it.
