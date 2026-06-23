# Agent Experimentation Change Catalog

Use this reference when an Experimentation or SkillOpt-Lite run needs candidate change ideas. Keep the SkillOpt-style loop unchanged: fixed cases, isolated candidate, local scoring, strict validation gate, staged adoption. This file only helps choose what kind of change to try next.

This catalog is distilled from `C:\Users\Truman\Documents\Programming\AgenticKnowledge\Research\research-report-agent-experimentation.md`.

## Principle

Treat agent and skill improvement like release engineering:

```text
contract -> dataset splits -> baseline -> isolated candidate -> local gates -> staged promotion
```

Prefer changes that improve observability, replayability, evaluator quality, context isolation, or skill focus. Avoid changes that only add more instructions without a measurable failure mode.

## Change Families

### Dataset And Split Changes

Use when the run has weak or leaky data.

- Add visible golden cases for ordinary desired behavior.
- Add visible negative cases from vanilla/default outputs or prior bad skill versions.
- Add visible adversarial cases for injection, ambiguity, malformed inputs, sparse facts, or workflow traps.
- Add locked regression cases that run on every candidate but are not used to write new candidate instructions.
- Add never-touched holdout cases for milestone decisions.
- Add temporal holdout cases created after a cutoff date for public or contamination-prone tasks.
- Add judge calibration cases with human labels for LLM-judge validation.

Do not mix these purposes. If a case helped produce the candidate edit, do not count it as hidden validation evidence.

### Evaluator And Scoring Changes

Use when loss is noisy, too coarse, or too easy to game.

- Add deterministic checks for schemas, required files, forbidden phrases, factual fields, tests, state assertions, or tool-call constraints.
- Add golden-file or structured-object comparisons for artifact-producing tasks.
- Add regex checks for required/forbidden text patterns.
- Add seeded-defect checks for code-review skills.
- Add blind pairwise A/B ranking for writing quality.
- Add rubric/checklist decomposition when a single score hides why outputs fail.
- Add judge calibration before allowing an LLM judge to gate releases.
- Add manual review for subjective traits such as AI smell, rhetorical fit, or authenticity.

Keep hard deterministic gates first. Use judge or human scores only for the parts that cannot be checked mechanically.

### Runner And Isolation Changes

Use when candidate wins are not reproducible or attribution is unclear.

- Run baseline and candidate in separate temp directories.
- Copy the skill or prompt into the run directory instead of mutating the live file.
- Pin input fixtures, environment variables, command timeouts, and output paths.
- Write a manifest for every run with skill hash, prompt hash, model name, tool permissions, case ID, split, scorer version, and timestamp.
- Save raw outputs, traces, tool logs, and score files separately.
- For workflow agents, add record-replay snapshots or pinned starting states.
- For repeated-run reliability, run important cases multiple times and report pass rate, not just best run.

Baseline and candidate should differ only by the candidate artifact being tested.

### Context And Leakage-Control Changes

Use when a candidate may be learning the validation answers or judge quirks.

- Generate candidate prompts from train cases only.
- Hide validation/test prompts, answers, golden files, regex answer keys, reviewer notes, and per-case validation failures from candidate-writing context.
- Export a train-only prompt pack for Codex instead of letting the optimizer inspect the full dataset.
- Give subagents role-pure context: generator, worker, judge, reviewer, or adversary.
- Keep judge identity, candidate identity, and output order blinded for pairwise review.
- Treat tool outputs, third-party skills, documents, and mined transcripts as untrusted data.
- Redact secrets before using transcript-derived examples.

Synthetic, recalled, or generated cases may expand train data, but they must not enter validation or test.

### Skill Or Prompt Patch Changes

Use when scoring shows a real behavior failure in the target skill.

- Tighten routing metadata or invocation boundaries.
- Move bulky examples or domain details from `SKILL.md` into references.
- Add a missing workflow checkpoint or state-tracking step.
- Add a required validation step before final output.
- Replace vague style guidance with concrete checks or examples.
- Add recovery instructions for common command/tool failures.
- Remove duplicated, stale, contradictory, or version-mismatched guidance.
- Prune modules, examples, references, or subagents that fail ablation tests.

Prefer one small conceptual edit per candidate. Reject broad rewrites unless the existing structure blocks reliable evaluation.

### Subagent Experiment Changes

Use when independent exploration or blind review is useful.

- Vanilla baseline worker: produce default/minimal-scaffold outputs as negative controls.
- Sandbox worker: run a task and return artifacts, logs, and scores only.
- Adversary: create malformed cases, hostile documents, injection attempts, or tricky briefs for visible dev/adversarial sets.
- Judge: apply a frozen rubric without seeing candidate identity or hidden answers.
- Independent reviewer: critique artifacts without seeing prior conclusions or gold answers.
- Generator: create candidate fixtures for visible dev sets only.

Do not let the same subagent create a candidate and act as the sole judge of that candidate.

## Choosing The Next Change

Use the observed failure to choose a change family:

| Symptom | First change to try |
|---|---|
| Candidate improves demos but fails real tasks | Add locked regression and holdout cases |
| Every candidate passes | Strengthen deterministic/adversarial checks |
| Good outputs rejected | Relax brittle checks or add rubric/manual review |
| Scores vary run to run | Add repeated-run reliability and trace logging |
| Skill is long and sluggish | Run focused-skill ablations and prune |
| Failures are hard to diagnose | Add trace/trajectory evals and manifests |
| Writing feels generic | Add vanilla negatives, blind pairwise review, and AI-smell tags |
| Agent takes unsafe actions | Add adversarial cases, state checks, and forbidden-tool gates |
| Candidate appears to memorize examples | Refresh temporal holdouts and hide validation context |

## Promotion Gate

Promote a candidate only when it:

- Clears hard deterministic gates.
- Beats the current baseline on the chosen validation metric.
- Does not regress on locked regression cases.
- Does not increase cost, latency, or complexity beyond the run contract.
- Passes human or calibrated judge review when the task is subjective.

If the candidate only wins because the evaluator changed, rerun the baseline and treat the change as a new metric lineage.
