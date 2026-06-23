# SkillOpt-Lite Implementation

Use this reference when the user wants SkillOpt-style live experimentation without heavy local ML, API-only training loops, large benchmark sweeps, or local vLLM serving.

## Purpose

SkillOpt-Lite separates the loop into two cheap pieces:

```text
Codex proposes small candidate edits
local machine scores fixed cases
strict gate accepts only real validation improvement
accepted candidates are staged for review
```

This is not a replacement for the full SkillOpt research trainer. It is a practical harness for consumer hardware and regular Codex usage.

## When To Use

Use this mode when:

- The user wants on-demand live experimentation.
- The target is a skill, prompt, agent workflow, or code behavior.
- A small local evaluator can be built from tests, golden files, regex checks, exact matches, or manual acceptance.
- The user wants to avoid API-heavy optimizer runs.

Do not use it when:

- No stable local or manual evaluator exists.
- The desired improvement cannot be reduced to cases and gates.
- The user expects full paper benchmark reproduction.
- The candidate writer would see hidden validation answers.

## Minimal Files

A run should have:

```text
.skillopt-lite/<run-id>/
  cases.jsonl
  baseline.json
  candidate.json
  staging/<timestamp>/
    manifest.json
    report.md
    proposed_SKILL.md
```

Each case is one JSON object:

```json
{
  "id": "unit-tests",
  "split": "val",
  "judge": {
    "type": "command",
    "command": "pytest -q",
    "cwd": "."
  }
}
```

Supported local judges:

- `command`: pass when the command exits with code 0.
- `regex`: pass when a pattern matches text or a file.
- `exact`: pass when actual text equals expected text.
- `golden`: pass when an actual file equals a golden file, with optional JSON normalization.
- `manual`: pass when `accepted` is true.

## On-Demand Loop

1. Create or review `cases.jsonl`.
2. Score the current target:

```bash
python scripts/skillopt_lite.py score --cases .skillopt-lite/run/cases.jsonl --split val --out .skillopt-lite/run/baseline.json
```

3. Ask Codex for a tiny candidate change, usually one to three edits.
4. Save the candidate skill or prompt as a separate file.
5. Score the candidate with the same cases and same split.
6. Gate the candidate:

```bash
python scripts/skillopt_lite.py gate \
  --current .skillopt-lite/run/baseline.json \
  --candidate .skillopt-lite/run/candidate.json \
  --candidate-artifact .skillopt-lite/run/candidate_SKILL.md \
  --live-artifact path/to/SKILL.md \
  --stage-dir .skillopt-lite/run/staging
```

7. Adopt only after user review:

```bash
python scripts/skillopt_lite.py adopt --staging .skillopt-lite/run/staging/<timestamp>
```

## Scoring Rules

Use `hard` for pass/fail cases. Use `soft` only when a deterministic partial-credit score exists. Use `mixed` for tiny validation sets where hard pass/fail is too coarse.

Default gate:

```text
candidate_score > current_score
```

Ties reject by default. If a tied candidate is simpler or cheaper, the user can adopt manually after reviewing the staged report.

## Hardware Budget

Safe defaults for a GTX 1070 / Ryzen 7600 / 32 GB RAM setup:

```yaml
cases_total: 6-12
validation_cases: 2-4
candidate_edits: 1-3
workers: 1
codex_calls_budget: 3-8
gate_metric: hard
auto_adopt: false
```

Increase case count before edit budget. Do not increase edit budget until the evaluator rejects bad candidates reliably.

## Leakage Rules

- Train cases can be summarized for Codex when asking for candidate edits.
- Validation cases should be withheld from candidate-writing context when possible.
- Never include hidden validation answers in the reflection prompt.
- Score baseline and candidate with the same commands and same files.
- Treat evaluator changes as a new metric lineage and rerun baseline.

## Failure Modes

- **Every candidate passes**: the evaluator is too weak; add stricter validation cases.
- **No candidate passes**: the edit budget may be too low, or the metric may be too coarse.
- **Candidate improves train but fails val**: reject and store the failure pattern.
- **Subjective output cannot be scored**: use `manual` cases or decompose the rubric into deterministic checks.
- **Codex budget burns too quickly**: use fewer cases, fewer edits, and one reflection call over grouped failures.
