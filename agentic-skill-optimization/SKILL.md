---
name: agentic-skill-scaffolding
description: Design and install ProPlay-inspired procedural-memory scaffolding for a new or existing Codex skill. Use when Codex needs to create, rename, reorganize, or reshape a target skill package so it can learn reusable procedures from successful episodes, run a preplay-execute-refine loop, automatically capture compact episode memory before final responses, support manual or Codex-mediated memory updates, and forward-test behavior with fresh Codex subagents without requiring API-based agent runners.
---

# Agentic Skill Scaffolding

## Contract

Transform a target skill into a ProPlay-inspired, Codex-native procedural memory skill. Do this by adding a lightweight structure that lets future Codex runs:

- Preplay: retrieve relevant procedural memory and sketch a task-specific path before acting.
- Execute: use that path as soft guidance while preserving normal reasoning and user instructions.
- Capture: default to automatic compact episode capture before the final response when there is reusable signal.
- Refine: update procedural memory from successful episodes, user corrections, validation results, or failed attempts with useful signal.
- Evaluate: launch fresh Codex subagents when available, pass only task-local context, and compare outputs before claiming improvement.

Do not recreate the ProPlay research repo or require OpenAI API keys. The scaffold must work through normal Codex skill usage, local files, and available Codex subagent/thread tools.

## Source Grounding

Before substantial scaffold design, read [references/proplay-source-map.md](references/proplay-source-map.md). Use it as the local bridge from the ProPlay paper and repository to Codex skill scaffolding.

When installing the default scaffold, prefer running [scripts/init_procedural_memory.py](scripts/init_procedural_memory.py) against the target skill instead of recreating the memory files by hand. Read [references/proplay-scaffold-template.md](references/proplay-scaffold-template.md) when customizing the generated files for a specific domain.

## Target Inspection

Read the target skill's `SKILL.md` completely. Then inspect only directly relevant bundled files:

- `references/` for domain rules, examples, rubrics, existing memory, or prior corrections.
- `scripts/` for deterministic helpers that should remain the source of truth.
- `assets/` for templates or output resources.
- `agents/openai.yaml` for user-facing metadata that may need to stay aligned.

Before editing, identify:

- Core task families the skill handles.
- Existing step sequence and validation gates.
- Places where reusable procedures would reduce drift or repeated re-discovery.
- Corrections, failure modes, or benchmark examples the user has supplied.
- Sensitive-data risks that should make auto-capture summarize, redact, or skip details.

Preserve the target skill's original purpose. Add procedural memory as scaffolding around the domain workflow, not as a replacement for it.

## Install The Scaffold

For the default scaffold, run:

```bash
python <this-skill>/scripts/init_procedural_memory.py <target-skill-path> --patch-skill
```

This creates:

```text
target-skill/
  SKILL.md
  references/
    procedure-memory.md
    procedure-graph.json
  scripts/
    record_episode.py
```

Then edit the generated `references/procedure-memory.md` so task-family names, examples, failure patterns, and training prompts match the target skill. Keep domain detail in the target skill's own references, not in this scaffolding skill.

Use `references/` so the memory is discoverable through standard skill progressive disclosure. Use the generated `scripts/record_episode.py` for before-final automatic capture unless the target skill already has a better deterministic memory updater.

## Capture Policy

Default every scaffolded target skill to `auto` capture. The target skill should record a compact memory episode before the final answer whenever the run contains reusable procedural signal.

Use these modes only when the user or domain requires them:

- `auto`: record by default before final response unless the episode is low-signal, sensitive, or would contaminate a held-out evaluation.
- `confirm`: draft the memory update and ask before writing when privacy, client data, job-search data, or user identity details are involved.
- `manual`: record only when the user explicitly asks.

For `auto`, the target skill must include a final-response receipt:

```text
Procedural memory: recorded episode_YYYYMMDD_short_slug.
```

or:

```text
Procedural memory: skipped because <specific reason>.
```

The receipt makes capture failures visible. Do not silently skip.

## Procedure Graph

The generated `references/procedure-graph.json` starts with:

```json
{
  "schema_version": 1,
  "skill": "target-skill-name",
  "capture_policy": {
    "mode": "auto",
    "before_final_required": true,
    "receipt_required": true,
    "sensitive_data": "summarize_or_skip"
  },
  "nodes": [],
  "edges": [],
  "episodes": [],
  "failure_patterns": []
}
```

Use stable ids such as `proc_audience_research` or `edge_research_to_draft`. Keep entries compact enough that Codex can inspect them directly.

Model each graph element after ProPlay's practical roles:

- Nodes: reusable procedural stages, not one-off actions.
- Edges: observed transitions where one procedure tends to enable another.
- Reliability: evidence-weighted confidence, not a universal truth claim.
- Episodes: compact records of task, outcome, procedures used, and evidence pointer.
- Failure patterns: context-sensitive traps to avoid during future preplay.

## Procedure Memory Reference

Create or update `references/procedure-memory.md` with these sections:

- Purpose: explain that the file supports a Codex-native preplay-execute-capture-refine loop.
- When to read: at the start of target-skill tasks that resemble prior episodes, after user corrections, and before subagent evaluations.
- Capture policy: default `auto`, before-final required, final receipt required, summarize or skip sensitive details.
- Graph schema: define nodes, edges, episodes, failure patterns, reliability, evidence, and capture policy.
- Preplay instructions: retrieve relevant nodes and edges, form a short plan, and treat it as soft guidance.
- Capture instructions: before final response, run `scripts/record_episode.py` or explicitly state a skip reason.
- Refine instructions: update memory only from meaningful signal; keep facts grounded in observed task outcomes.
- Training instructions for the user: show how to seed examples, run practice episodes, opt out of capture, approve sensitive updates, and request subagent checks.
- Contamination rules: keep evaluation prompts and hidden expected answers out of training memory until they are spent.

Do not store long transcripts in the procedure graph. Summarize them into reusable procedures and evidence pointers.

## SKILL.md Integration

Patch the target `SKILL.md` with a short section near the top-level workflow. Keep the exact wording domain-specific, but include this behavior:

```markdown
## Procedural Memory

For tasks that resemble prior episodes, read `references/procedure-memory.md` and inspect `references/procedure-graph.json` before drafting the task plan.

Use the procedure graph to preplay a likely path: select relevant procedure nodes, note reliable transitions, and identify failure patterns to avoid. Treat the preplay as soft guidance; user instructions and fresh task evidence override stale memory.

Default to automatic capture. Before the final response, record a compact episode with `scripts/record_episode.py` when the run contains reusable procedural signal. Skip only when the episode is low-signal, sensitive beyond safe summarization, or part of a held-out evaluation that should remain uncontaminated.

End with a procedural-memory receipt: `recorded <episode_id>` or `skipped because <reason>`.
```

If the target skill already has a workflow, insert the memory step before execution and the capture step after validation but before the final response. If the target skill is tiny, keep the section shorter but preserve the before-final capture gate and receipt.

## Training Plan

When finishing the scaffold, give the user concrete training instructions:

1. Seed memory with 3-5 representative tasks, including at least one failure or correction if available.
2. Run the target skill on one real task at a time.
3. Let the target skill auto-record compact memory by default before each final response.
4. For sensitive episodes, switch that episode to confirm mode and approve or edit the proposed memory record.
5. After several updates, run fresh subagent evaluations on held-out prompts.

Give the user copyable prompts such as:

```text
Use $target-skill on this task and auto-record a compact procedural-memory episode unless it is low-signal or sensitive.
```

```text
Update $target-skill procedural memory from this correction. Store only reusable procedures, transition evidence, and failure patterns.
```

```text
For this run, do not record procedural memory. Treat it as held-out evaluation.
```

```text
Forward-test $target-skill with a fresh Codex subagent on this held-out task. Do not reveal expected answers or prior diagnosis.
```

## Subagent Evaluation

When Codex subagent tools are available, use them for forward-testing after installing or updating the scaffold. If the tools are not already visible, search for multi-agent or subagent tools first.

Use fresh subagents and neutral prompts:

```text
Use $target-skill at <absolute-target-skill-path> to complete this user request:
<held-out task>
```

For before/after comparisons:

- Keep a baseline copy of the target skill before memory changes when practical.
- Run the same held-out task against baseline and scaffolded variants.
- Disable auto-capture for held-out evaluation tasks unless the benchmark is spent.
- Do not tell subagents which variant is expected to win.
- Pass raw task artifacts, not your diagnosis or intended fix.
- Score hard gates first, then quality, then process compliance.
- Claim improvement only when the scaffolded version wins or ties with a clear reliability, cost, maintainability, or process advantage.

If subagent tools are unavailable, provide the exact prompts the user can run later and say validation is pending.

## Update Policy

Keep procedural memory useful and clean:

- Add a node only for a reusable stage, not a one-off action.
- Add or strengthen an edge only when there is observed evidence that one procedure reliably enables another.
- Record failures as avoidable patterns with context, not blame or vague warnings.
- Auto-record compact episodes by default, but skip or ask confirmation for sensitive details, private user data, and clean held-out evaluations.
- Prefer small updates after each episode over large retrospective rewrites.
- Avoid storing private, sensitive, or irrelevant user data in memory.
- Do not add benchmark holdout answers, evaluator rubrics, or hidden expected outputs to memory until the evaluation is no longer meant to be clean.

## Validation

After editing a target skill:

- Validate YAML frontmatter and skill naming with the standard skill validator when available.
- Check that `references/procedure-memory.md`, `references/procedure-graph.json`, and `scripts/record_episode.py` exist in the target skill.
- Confirm `agents/openai.yaml`, if present, still matches the target skill's purpose.
- Run a JSON parse check on `references/procedure-graph.json`.
- Run `scripts/record_episode.py --help` or a harmless test against a temporary graph.
- Report installed paths, memory files created, capture mode, training prompts, subagent evaluation status, and any validation result.

If the user asked only for a scaffold design and not file edits, provide the proposed file tree, patches, and training plan without modifying files.