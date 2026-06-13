# Skill Package Optimization

Use this reference when the experiment target is a filesystem-based skill, prompt package, agent workflow, or reusable instruction bundle.

## Contents

- [Core Model](#core-model)
- [Target Package Shape](#target-package-shape)
- [Intake](#intake)
- [Goal Spec](#goal-spec)
- [Evaluation Design](#evaluation-design)
- [Lifecycle](#lifecycle)
- [Risk Rules](#risk-rules)

For a broader catalog of experiment patterns, dataset splits, subagent roles, and release gates, read `experimentation-patterns.md` before designing a substantial skill optimization run.

## Core Model

Treat skill improvement as experimental software engineering:

1. Convert the user's vague improvement goal into measurable acceptance criteria.
2. Build or identify a baseline evaluation suite before editing the target skill.
3. Generate small, isolated variants tied to one hypothesis each.
4. Run variants in clean branches, worktrees, containers, or scratch copies.
5. Score with deterministic checks first, decomposed LLM judging second, and human review gates where needed.
6. Keep only changes that improve the primary metric without violating regressions, safety, cost, or latency constraints.
7. Write durable memory: what was tried, what failed, what worked, and why.

Use the outer loop discipline from autoresearch-style loops: one task or hypothesis per clean-context iteration, explicit pass/fail backpressure, persistent state in files and git, and stop conditions. Do not substitute loop machinery for evaluator design. A weak metric optimizes the wrong behavior faster.

## Target Package Shape

Understand a skill as a package, not a single prompt:

```text
<skills-root>/<target-skill>/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
  evals/
  experiments/<YYYYMMDD-HHMM-objective>/
    PLAN.md
    experiment_state.json
    baseline/
    variants/
    traces/
    RESULTS.md
    PATCH.md
    LEARNINGS.md
```

Keep `SKILL.md` concise and frequently loadable. Move detailed domain principles, examples, rubrics, failure modes, fixtures, and scripts into references or eval directories that are loaded only when needed.

## Intake

If the user has not already specified enough detail, ask only for the missing pieces needed to build an experiment plan:

- Target skill path or name.
- Specific behavior to improve, ideally with bad and good examples.
- Protected behaviors that must not get worse: factuality, safety, tone, cost, latency, recall, false positives, formatting, or tool protocol compliance.
- Budget: iterations, variants, trials per variant, wall-clock time, or cost.
- Edit permission: `SKILL.md`, references, scripts, evals, or propose-only.
- Approval policy: approve plan before running, approve final patch before merge, and always approve self-modification before applying.

Use these defaults when the user delegates:

```yaml
budget_defaults:
  max_iterations: 5
  max_variants_per_iteration: 3
  trials_per_variant: 3
  max_wall_clock_minutes: 45
  approval_policy:
    before_first_run: required
    before_merging_patch: required
    before_self_modification: required
```

## Goal Spec

Turn intake into an explicit contract before editing:

```yaml
goal_spec:
  user_goal: "Make the cover-letter skill generate less generic text."
  target_skill: "path/to/skill"
  goal_type: style_quality | security_detection | process_compliance | routing | efficiency | self_optimization | mixed
  risk_level: low | medium | high
  primary_metric:
    name: "specificity_without_fabrication"
    direction: maximize
    score_formula: "0.35*job_alignment + 0.25*user_voice + 0.20*concrete_evidence + 0.10*generic_phrase_penalty_inverted + 0.10*format_compliance"
  hard_gates:
    - "No fabricated experience, employers, credentials, or metrics."
    - "Must preserve required tool sequence."
  regression_metrics:
    - factuality
    - tone
    - length_limit
    - privacy
  permissions:
    may_edit_skill_md: true
    may_edit_references: true
    may_edit_scripts: true
    may_edit_evals: true
    may_use_network: false
    may_use_secrets: false
  confirmation_required: true
```

## Evaluation Design

Prefer layered evaluation:

- Structural checks: frontmatter validity, skill naming, linked reference existence, no large accidental files, no stale UI metadata.
- Deterministic behavior checks: required sections, banned phrases, tool-call protocol, generated file existence, formatting constraints, parseability, fixture pass/fail.
- Golden cases: stable prompts that represent desired ordinary behavior.
- Adversarial cases: edge cases, attack/noise cases, regression examples, missing-context scenarios.
- Vanilla subagent baselines: raw outputs from isolated default subagents given real task inputs and a minimal ordinary prompt, used to capture the default failure distribution before writing new gates.
- Holdout cases: kept away from variant-writing context when possible.
- LLM judging: decomposed rubric with separate scores for each dimension, raw judge outputs saved, and clear tie-breaking rules.

Use `experimentation-patterns.md` to choose additional evaluation patterns when needed: locked regression suites, blind pairwise ranking, metamorphic perturbation tests, property/fuzz tests, step/final/trajectory evals, record-replay snapshots, repeated-run reliability, judge calibration, temporal holdouts, focused ablations, and human AI-smell panels.

Never compare a baseline scored with one evaluator to a variant scored with a changed evaluator. Treat evaluator changes as infrastructure, rerun the baseline, and mark the metric lineage clearly.

### Vanilla Subagent Baselines

Use this pattern when optimizing writing, prompt, agent, or skill behavior and the user explicitly authorizes subagents. The goal is to see what a normal under-scaffolded model produces, not to get the best output.

Procedure:

1. Select realistic stored inputs from the target workflow, such as actual job descriptions, support tickets, prompts, user profiles, or prior application packets.
2. Build the smallest shared context packet the ordinary workflow would plausibly receive. Include the task facts, but do not include the target skill, evaluator rubric, known anti-patterns, desired fixes, or examples of the preferred output.
3. Spawn isolated default subagents with the minimal normal user request, such as `make a cover letter for this job`, `write a reply to this customer`, or `summarize this incident`.
4. If the system would otherwise invoke tools or specialized skills, constrain only the execution surface: `Answer in chat only. Do not use tools, files, skills, web, validation, or export.` Keep this constraint identical across agents.
5. Save each raw output with provenance: source input path/URL, application or case id, prompt shape, subagent id, date, and whether tools/skills were disabled.
6. Run the current evaluator against these outputs and record which failures are caught, missed, or over-flagged.
7. Convert caught and missed failures into negative controls, candidate audit rules, or judge rubric items. Keep at least some raw outputs as holdouts and do not leak them into future variant instructions.

Contamination rules:

- Discard or separately label any output where the subagent used the target skill, browsed, created files, exported artifacts, ran validators, or received the desired anti-pattern list.
- Do not "humanize" or repair negative examples before saving them. Their value is that they preserve natural model mistakes.
- Do not overfit the skill to one batch. Use the batch to identify failure families, then test against separate golden, adversarial, and holdout cases.

## Lifecycle

### Phase A: Inspect

Read only enough to understand the target skill:

1. `SKILL.md` frontmatter and body.
2. References explicitly linked by `SKILL.md`.
3. Existing scripts, evals, and UI metadata.
4. Recent experiment logs or prior learnings.

Write `experiments/<id>/PLAN.md` and `experiment_state.json` when the run is substantial.

### Phase B: Baseline

Before editing, run the current target skill against the evaluation suite. Include deterministic checks, sample outputs, judge prompts and raw scores when used, trace summaries, and top failure modes.

Baseline summary shape:

```json
{
  "baseline_id": "baseline-001",
  "target_commit": "<git_sha>",
  "cases_total": 40,
  "hard_gate_pass_rate": 0.88,
  "primary_score_mean": 0.61,
  "primary_score_ci95": [0.57, 0.65],
  "regressions": [],
  "top_failure_modes": ["generic opening", "insufficient user facts"]
}
```

### Phase C: Plan Variants

Generate small variants. Each variant should change one conceptual lever and include its expected causal mechanism.

Good variant families:

- Routing: sharpen description metadata, trigger language, or invocation boundaries.
- Progressive disclosure: move bulky details out of `SKILL.md`, add clear reference-selection rules, remove duplicated guidance.
- Workflow reliability: add required checkpoints, tool sequence constraints, recovery paths, or state tracking.
- Evaluation: add golden cases, adversarial cases, deterministic lint, or judge rubrics.
- Output quality: add evidence extraction, failure-mode checks, examples, reviewer passes, or final revision gates.
- Efficiency: reduce context load, merge redundant steps, replace repeated manual code with scripts.

### Phase D: Confirm

Before autonomous edits, show the objective, target path, metric, hard gates, variants, budget, sandbox permissions, merge policy, and expected artifacts. The user can approve, change constraints, or cancel.

### Phase E: Run Variants

For each variant:

1. Create a branch, worktree, or scratch copy from the same base.
2. Apply the variant patch.
3. Run structural skill lint.
4. Run deterministic evals.
5. Run LLM judge evals only after deterministic gates pass, unless judge failure is the target.
6. Store traces and outputs.
7. Keep the variant isolated until winner selection.

### Phase F: Select Winner

Use this tiered rule:

1. Reject hard-gate failures.
2. Reject protected-regression failures.
3. Choose the best primary metric gain.
4. Prefer the smaller and more maintainable patch for close scores.
5. Escalate low-confidence or close qualitative calls to the user.

### Phase G: Patch And Memory

Produce or update:

- `PATCH.md`: human-readable diff summary and rationale.
- `RESULTS.md`: metrics, failed variants, trace links, and caveats.
- `LEARNINGS.md`: durable memory for future optimization.
- The accepted skill patch, only after the approval policy allows it.

## Risk Rules

- Do not edit production secrets, hidden holdout evals, or unrelated user work.
- Do not leak holdout cases into instructions intended for future agents.
- Do not stuff examples into `SKILL.md` when references or eval fixtures are better.
- Do not keep a variant that wins by weakening safety, factuality, privacy, or user intent.
- Do not let LLM judges decide alone when deterministic evidence can be added.
- For self-optimization, require explicit user approval before applying the final patch.
