# SkillOpt-Sleep Pattern

Use this reference when the experiment target is a live agent workflow that should improve from prior sessions, nightly/offline replay, or Codex/Claude transcript history. This pattern adapts SkillOpt-Sleep's deployment-time loop rather than the paper benchmark trainer.

## Contents

- [Fit](#fit)
- [Two Modes](#two-modes)
- [Sleep Mode](#sleep-mode)
- [On-Demand Mode](#on-demand-mode)
- [Core Loop](#core-loop)
- [Architecture](#architecture)
- [Correction Dataset](#correction-dataset)
- [Task Records](#task-records)
- [Backend Contract](#backend-contract)
- [Replay And Scoring](#replay-and-scoring)
- [Consolidation And Gate](#consolidation-and-gate)
- [Dream And Recall](#dream-and-recall)
- [Staging And Adoption](#staging-and-adoption)
- [Budget Defaults](#budget-defaults)
- [Implementation Notes](#implementation-notes)
- [Failure Modes](#failure-modes)

## Fit

Prefer this pattern when the user asks to:

- Improve a Codex, Claude Code, or local agent from past sessions.
- Run an overnight, sleep, dream, replay, or self-evolution cycle.
- Mine recurring tasks from transcripts and update a skill or memory file.
- Avoid API-backed training while spending only local agent/Codex budget.
- Build a lightweight SkillOpt-like loop around local tests, golden files, or human review.

Use regular skill-package optimization when the user already has a fixed eval suite and wants isolated variants of one skill. Use the Sleep pattern when the eval set is mined from agent usage or replayed from recent tasks.

## Two Modes

Support two distinct operating modes:

- **Sleep mode** is automatic and retrospective. It scans old chats/session archives, extracts corrections and reusable lessons, builds a replay dataset, proposes skill or memory edits, gates them, and stages them for review.
- **On-demand mode** is live and user-directed. It behaves more like SkillOpt: the user asks to improve a target now, Codex establishes the metric and split, runs controlled experiments, and returns a measured patch or recommendation.

Do not blur the modes. Sleep mode optimizes from accumulated evidence without needing a new user instruction for every hypothesis. On-demand mode starts from the user's current objective and should not mine unrelated old chats unless the user requests that context.

## Sleep Mode

Use Sleep mode for automatic skill evolution from prior usage.

Inputs:

- Archived Codex/Claude sessions or chat transcripts.
- Current skill files, memory files, or project instructions to improve.
- Optional user preferences about which skills may be touched.
- Local checks, command evaluators, golden examples, or manual-review fields.

Harvest these signals, in priority order:

1. Explicit user corrections: "not that", "change this to", "you missed", "don't say", "use X instead", direct rewrites, or final accepted wording.
2. Accepted final artifacts after earlier rejected drafts.
3. Repeated assistant failures followed by successful repair steps.
4. Tool/test/lint failures that later pass.
5. User-stated preferences or constraints that recur across sessions.
6. Reasoning, trace summaries, or trajectory notes when they are present in local logs and useful for reconstructing the failure mode.

Treat hidden or unavailable model chain-of-thought as unavailable. Use only transcript content, trace summaries, tool logs, command output, saved artifacts, or user-visible reasoning that exists locally.

Sleep mode output is a staged proposal, not a live mutation:

```text
old chats -> correction events -> task records -> train/val split
  -> replay current skill -> reflect bounded edits -> gate
  -> .skillopt-sleep/staging/<timestamp>/report.md
  -> user adopts or discards
```

Default policy:

- Run with `backend: mock` or local checks first when building plumbing.
- Use `backend: codex` only for bounded real reflection/replay calls.
- Keep `auto_adopt: false` unless the user explicitly enables it.
- Never apply edits that only summarize one session; require recurring or validated behavior.

## On-Demand Mode

Use On-demand mode for live, user-directed improvement.

Inputs:

- A current target: code, prompt, skill, workflow, benchmark, or agent behavior.
- A user-approved goal and metric.
- A bounded budget: iterations, time, tasks, or Codex calls.
- A fixed evaluator or a small evaluator built before editing.

Loop:

```text
user objective -> baseline -> one hypothesis -> isolated variant
  -> run evaluator -> keep/discard -> log result -> next hypothesis
```

For skill files, on-demand mode can use the same bounded-edit and gate machinery as Sleep mode, but the dataset should come from the current user-approved eval suite, not automatically mined old chats. Read `skill-optimization.md` when the target is a filesystem skill package and use this reference when the user specifically wants Sleep-style replay, staged adoption, or transcript-mined evidence.

## Core Loop

One Sleep cycle:

```text
harvest transcripts
  -> mine recurring/checkable tasks
  -> replay tasks under current skill/memory
  -> reflect over failures and successes
  -> propose bounded edits
  -> gate candidate on held-out tasks
  -> stage proposal
  -> user adopts or discards
```

Keep this contract intact:

1. Do not mutate live skills during harvest, replay, or consolidation.
2. Split mined tasks into train and validation before reflection.
3. Use train tasks to propose edits.
4. Use validation tasks only to accept or reject the candidate.
5. Stage accepted edits with a report and backup path.
6. Require explicit adoption unless the user has opted into auto-adopt.

## Architecture

Minimal project layout:

```text
<project>/
  .agents/skills/<target-skill>/SKILL.md
  .skillopt-sleep/
    state.json
    correction_events.jsonl
    task_archive.jsonl
    staging/<YYYYMMDD-HHMMSS>/
      manifest.json
      report.md
      report.json
      proposed_SKILL.md
      backup/
```

Recommended engine modules:

```text
config.py        safe defaults and CLI/config overrides
harvest.py       transcript/session discovery and secret redaction
corrections.py   extract user corrections, accepted rewrites, and repair traces
mine.py          convert correction events into checkable TaskRecord objects
replay.py        run tasks against current and candidate skill
backend.py       attempt, judge, and reflect operations
dream.py         recall similar past tasks and create train-only variants
gate.py          strict held-out accept/reject decision
staging.py       write proposals and adopt with backup
state.py         night counter, last harvest time, task archive
```

## Correction Dataset

In Sleep mode, first build a correction-event dataset before task records. Store one JSON object per event:

```json
{
  "id": "corr-001",
  "session_id": "019...",
  "timestamp": "2026-06-22T03:17:00-07:00",
  "project": "C:/path/to/project",
  "skill_hint": "cover-letter",
  "source": "codex_archived_session",
  "bad_behavior": "Assistant used a generic opener.",
  "correction": "User rewrote opener with concrete company-specific context.",
  "accepted_behavior": "Final draft starts with the specific project and role motivation.",
  "evidence": "short transcript excerpt or artifact path",
  "tags": ["user-correction", "style", "specificity"],
  "confidence": 0.82
}
```

Convert correction events into task records only when they imply a reusable behavior and an evaluator can be defined. Examples:

- A rewrite can become a golden-output or rubric case.
- A failed command followed by a passing command can become a command-check case.
- A formatting correction can become a regex/structural case.
- A repeated preference can become a rule-judge case.

Do not create skill edits directly from corrections. Corrections are evidence; gated replay decides what ships.

## Task Records

Represent every mined/replayed task as structured data:

```json
{
  "id": "task-001",
  "project": "C:/path/to/project",
  "intent": "Fix the parser bug and keep tests passing.",
  "context_excerpt": "Relevant transcript, files, or failure summary.",
  "reference_kind": "command|exact|regex|rubric|manual|rule",
  "reference": "pytest tests/test_parser.py",
  "judge": {"type": "command", "command": "pytest tests/test_parser.py"},
  "system": "",
  "tags": ["python", "tests"],
  "split": "train",
  "origin": "real",
  "derived_from": "corr-001"
}
```

Split semantics:

- `train`: visible to reflection and edit generation.
- `val`: held out for the validation gate.
- `test`: never used during consolidation; score only for final reporting.
- `dream`: synthetic or recalled training material; never enters validation/test.

## Backend Contract

Backends supply three operations:

```python
class Backend:
    def attempt(self, task, skill: str, memory: str, sample_id: int = 0) -> str:
        ...

    def judge(self, task, response: str) -> tuple[float, float, str]:
        ...

    def reflect(
        self,
        failures,
        successes,
        skill: str,
        memory: str,
        *,
        edit_budget: int,
        evolve_skill: bool,
        evolve_memory: bool,
    ) -> list[EditRecord]:
        ...
```

Use a mock backend for plumbing tests. A useful mock backend should solve a task only when the needed rule text is present in `skill + memory`, score locally, and propose the missing rule for failed tasks. This proves the loop, gate, and staging without external spend.

For Codex-only runs, implement the real backend by shelling out to `codex exec` for `attempt` and `reflect`, while keeping `judge` local whenever possible. Use `codex exec -o <file>` or JSON output schemas so downstream parsing is stable.

## Replay And Scoring

Replay compares the current skill and candidate skill against the same task slice:

```python
def replay_batch(backend, tasks, skill, memory):
    pairs = []
    for task in tasks:
        response = backend.attempt(task, skill, memory)
        hard, soft, reason = backend.judge(task, response)
        pairs.append((task, ReplayResult(response, hard, soft, reason)))
    return pairs
```

Prefer local judges, in this order:

1. Command/test checks: `pytest`, `npm test`, `ruff`, `mypy`, `cargo test`.
2. Golden file or structured object comparison.
3. Regex or required-output checks.
4. Rule-based judge for tool calls, sections, length, or exact formatting.
5. Manual `accepted: true/false` for subjective cases.
6. LLM/rubric judge only when no deterministic judge is credible.

Cache replay by `(task_hash, skill_hash, memory_hash, sample_id)` so validation re-scoring is cheap and reproducible.

## Consolidation And Gate

Consolidation is one bounded SkillOpt epoch:

```text
score baseline on val
run train tasks
split train results into failures/successes
ask backend.reflect for at most edit_budget edits
apply edits to a candidate copy
score candidate on val
accept only if candidate_score > baseline_score
```

Gate score:

```python
def select_gate_score(hard, soft, metric="mixed", mixed_weight=0.5):
    if metric == "hard":
        return hard
    if metric == "soft":
        return soft
    return (1.0 - mixed_weight) * hard + mixed_weight * soft
```

Strict gate:

```python
if candidate_score > current_score:
    accept_candidate()
else:
    reject_candidate()
```

Keep rejected edits as negative feedback in the report or state. Do not ship them.

## Dream And Recall

Use dream and recall only as training-signal amplifiers:

- `dream_rollouts > 1`: run each train task multiple times and learn from good-vs-bad contrast.
- `recall_k > 0`: retrieve similar historical tasks from the archive and add them to train.
- `dream_factor > 0`: create lightweight train-only variants of real tasks.

Never allow recalled or synthetic tasks into validation or test slices. That is the main leakage guard.

A cheap local recall baseline is lexical Jaccard over task intent tokens. Upgrade to local embeddings only if lexical recall misses obvious recurring task families.

## Staging And Adoption

Stage every accepted proposal:

```text
.skillopt-sleep/staging/<timestamp>/
  manifest.json
  report.md
  report.json
  proposed_SKILL.md
  proposed_CLAUDE.md or proposed_MEMORY.md
```

`manifest.json` should include:

```json
{
  "live_skill_path": ".agents/skills/example/SKILL.md",
  "live_memory_path": "CLAUDE.md",
  "has_skill": true,
  "has_memory": false,
  "accepted": true
}
```

Adoption copies staged files over live paths only after backing up existing files into the staging directory. Default to review-gated adoption. Use auto-adopt only for low-risk, deterministic eval suites.

## Budget Defaults

Use conservative defaults on small hardware or Codex-budget-only setups:

```yaml
mode: sleep | on-demand
max_sessions_per_night: 15
max_tasks_per_night: 5
holdout_fraction: 0.34
edit_budget: 1-3
gate_metric: mixed
gate_mixed_weight: 0.5
dream_rollouts: 1
recall_k: 0
dream_factor: 0
auto_adopt: false
backend: mock first, codex only after dry-run
```

Increase in this order:

1. More real tasks.
2. `recall_k` for relevant historical examples.
3. `dream_rollouts` for noisy stochastic agents.
4. Edit budget.

Do not increase edit budget before the gate and evaluator are trustworthy.

## Implementation Notes

- Store state outside the live skill so failed nights do not affect the agent.
- Redact secrets during harvest before any reflection call.
- Keep task mining conservative: prefer checkable tasks over interesting but unscoreable sessions.
- Filter mined tasks to the target skill when optimizing one specific skill.
- Keep optimizer prompts output-only JSON and validate against a schema.
- Append learned rules to a clear "Learned preferences" or "Learned procedures" block instead of rewriting the whole skill.
- Include task output contracts in reflection prompts so the optimizer cannot learn impossible rules.
- Use `codex exec --sandbox read-only` for reflection/judging and `--sandbox workspace-write` only for replay tasks that need file edits.
- Use `--skip-git-repo-check` only inside isolated scratch directories or known-safe temp workspaces.
- Never compare a candidate against a baseline scored on a different task split or changed judge.

## Failure Modes

- **No checkable tasks mined**: broaden harvest lookback or ask the user for task examples and local checks.
- **Corrections do not imply reusable tasks**: store them as notes, but do not turn them into edits until recurrence or an evaluator exists.
- **Candidate sounds good but gate rejects**: keep the rejection; add failure details to negative feedback.
- **Gate always accepts vague rules**: evaluator is too weak. Add deterministic checks or stricter validation cases.
- **Edits overfit to transcript details**: require general rules and ban task IDs, exact answers, file names, and one-off constants unless they are stable project conventions.
- **Codex budget burns too quickly**: lower max tasks, cache replay, use mock dry-runs, keep local judges, and batch reflection.
- **Skill bloats**: prefer replace/delete edits, move long examples into references, and cap learned block length.
- **Subjective quality cannot be judged locally**: require manual review records or a calibrated rubric before allowing auto-adopt.