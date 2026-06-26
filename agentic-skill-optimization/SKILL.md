---
name: agentic-skill-scaffolding
description: Design and install ProPlay-inspired procedural-memory scaffolding for a new or existing Codex skill. Use when Codex needs to create, rename, reorganize, or reshape a target skill package so it can learn reusable procedures from successful episodes, run a retrieve-preplay-execute-capture-refine loop with required dense embeddings plus Reciprocal Rank Fusion (RRF), automatically capture compact episode memory before final responses, require explicit confirmation before skipping capture, and forward-test behavior with fresh Codex subagents without API-based agent runners.
---

# Agentic Skill Scaffolding

## Contract

Transform a target skill into a ProPlay-inspired, Codex-native procedural memory skill. Add a local structure that lets future Codex runs:

- Retrieve: run required local dense embedding retrieval and RRF retrieval before preplay, then blend scores as 75% normalized RRF and 25% normalized dense similarity.
- Preplay: use the retrieved memory pack and task-specific transition reliability to sketch a task-specific path before acting.
- Execute: use that path as soft guidance while preserving normal reasoning, user instructions, and fresh observations.
- Capture: default to automatic compact episode capture before the final response when there is reusable signal, including planned trace, executed trace, outcome/reward, productive prefix, and failed suffix when available.
- Confirm skip: never skip capture unless the user explicitly confirms skipping for that run.
- Refine: run a local refinement script that updates procedure nodes, observed edges, reward-weighted transition reliability records, and failure patterns from successful episodes, user corrections, validation results, or failed attempts with useful signal.
- Interface: support optional local environment adapters or deterministic scripts for tasks that can expose observations, actions, validation signals, or rewards.
- Evaluate: launch fresh Codex subagents when available, pass only task-local context, and compare outputs before claiming improvement.

Prefer porting ProPlay's local mechanics over reducing them to prose. Do not require paid API calls, OpenAI API keys, or benchmark services by default. The scaffold must work through normal Codex skill usage, local files, available Codex subagent/thread tools, optional local environment adapters, and a required local embedding backend.

## Source Grounding

Before substantial scaffold design, read [references/proplay-source-map.md](references/proplay-source-map.md). Use it as the local bridge from the ProPlay paper and repository to Codex skill scaffolding.

When installing the default scaffold, prefer running [scripts/init_procedural_memory.py](scripts/init_procedural_memory.py) against the target skill instead of recreating the memory files by hand. Read [references/proplay-scaffold-template.md](references/proplay-scaffold-template.md) when customizing generated files for a specific domain.

## Target Inspection

Read the target skill's `SKILL.md` completely. Then inspect only directly relevant bundled files:

- `references/` for domain rules, examples, rubrics, existing memory, or prior corrections.
- `scripts/` for deterministic helpers that should remain the source of truth.
- `assets/` for templates or output resources.
- `agents/openai.yaml` for user-facing metadata that may need to stay aligned.

Before editing, identify core task families, existing validation gates, places where reusable procedures would reduce drift, and privacy risks that should make auto-capture summarize or ask for explicit skip confirmation.

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
    retrieve_memory.py
    record_episode.py
    refine_graph.py
```

Then edit the generated `references/procedure-memory.md` so task-family names, examples, failure patterns, and training prompts match the target skill. Keep domain detail in the target skill's own references, not in this scaffolding skill.

## Retrieval Policy

Default every scaffolded target skill to hybrid retrieval with required embeddings:

```bash
python scripts/retrieve_memory.py references/procedure-graph.json --query "<current task summary>" --top-k 8 --inject-k 3
```

The generated retriever must use local `sentence-transformers` embeddings and RRF. It blends candidate scores as:

```text
final_score = 0.75 * normalized_rrf_score + 0.25 * normalized_dense_score
```

Use `sentence-transformers/all-MiniLM-L6-v2` by default. If the embedding backend or model is unavailable, retrieval should fail clearly with setup instructions rather than silently falling back to lexical-only retrieval.

For procedure transitions, combine the hybrid retrieval score with local task-specific reliability when reliability records exist. Task-specific reliability is computed from local task embeddings accumulated from observed outcomes, not from API calls.

Inject only the compressed top results into preplay: similar failures, avoidance rules, relevant procedure transitions, and reliability evidence. Treat retrieved memory as soft guidance, not commands.

## Capture Policy

Default every scaffolded target skill to `auto` capture. The target skill should record a compact memory episode before the final answer whenever the run contains reusable procedural signal.

When available, capture these ProPlay-like fields:

- `planned_trace`: procedure ids or compact procedure objects from preplay.
- `executed_trace`: procedure ids or compact procedure objects representing what actually happened.
- `outcome` and `reward`: validation, user correction, benchmark score, test result, or a local heuristic score.
- `productive_prefix`: the useful prefix of the executed trace when the full run only partially succeeded.
- `failure_suffix`: the failed or corrected suffix when a trap should be retrieved later.
- `procedure_candidates`: reusable procedure nodes Codex inferred from the run.
- `failure_patterns`: compact avoidable patterns with context and avoidance rules.

Skipping capture requires explicit user confirmation for that run. If the agent believes capture should be skipped because the episode is low-signal, sensitive, or part of held-out evaluation, it must ask the user to confirm the skip before finalizing. If confirmation is unavailable, record a minimal sanitized episode instead of silently skipping.

The final response must include one receipt:

```text
Procedural memory: recorded episode_YYYYMMDD_short_slug.
```

or, only after explicit user confirmation:

```text
Procedural memory: skipped by explicit user confirmation because <specific reason>.
```

Do not silently skip.

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
    "skip_requires_confirmation": true,
    "sensitive_data": "summarize_or_confirm_skip"
  },
  "retrieval_policy": {
    "method": "hybrid_rrf_dense_reliability",
    "rrf_weight": 0.75,
    "dense_weight": 0.25,
    "dense_required": true,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "default_top_k": 8,
    "inject_k": 3,
    "rrf_k": 60,
    "rankers": ["lexical", "procedure_overlap", "failure_pattern_match"],
    "reliability_weight": 0.15
  },
  "nodes": [],
  "edges": [],
  "episodes": [],
  "failure_patterns": [],
  "environment_interfaces": [],
  "refinement_policy": {
    "method": "local_trace_reward_reliability",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "api_calls_required": false
  }
}
```

Use stable ids such as `proc_audience_research` or `edge_research_to_draft`. Keep entries compact enough that Codex can inspect them directly.

Model each graph element after ProPlay's practical roles:

- Nodes: reusable procedural stages, not one-off actions.
- Edges: observed transitions where one procedure tends to enable another.
- Reliability: evidence-weighted confidence and task-specific reliability embeddings, not a universal truth claim.
- Episodes: compact records of task, outcome/reward, planned trace, executed trace, productive prefix, failure suffix, procedures used, lessons, failure patterns, and evidence pointer.
- Failure patterns: context-sensitive traps to avoid during future preplay.
- Environment interfaces: optional local adapters or scripts that expose observations, actions, validation, or rewards without paid API calls.

## Procedure Memory Reference

Create or update `references/procedure-memory.md` with these sections:

- Purpose: explain that the file supports a Codex-native retrieve-preplay-execute-capture-refine loop.
- When to read: at the start of target-skill tasks that resemble prior episodes, after user corrections, and before subagent evaluations.
- Retrieval instructions: run `scripts/retrieve_memory.py` with required embeddings plus RRF before preplay and inject only compressed top results.
- Capture policy: default `auto`, before-final required, final receipt required, explicit confirmation required to skip.
- Graph schema: define nodes, edges, episodes, failure patterns, retrieval policy, reliability, evidence, and capture policy.
- Preplay instructions: use retrieved failures, nodes, and edges to form a short plan; treat it as soft guidance.
- Capture instructions: before final response, run `scripts/record_episode.py`; ask for explicit confirmation before any skip.
- Refine instructions: after capture, run `scripts/refine_graph.py` to update nodes, edges, reliability records, and failure patterns from the observed episode. Keep facts grounded in observed task outcomes.
- Environment instructions: when a task has a deterministic helper, local simulator, test suite, validator, or benchmark wrapper, treat it as an optional local environment adapter and record its observations/actions/rewards in the episode summary.
- Contamination rules: keep evaluation prompts and hidden expected answers out of training memory until they are spent; user-provided "do not record" is explicit skip confirmation.

Do not store long transcripts in the procedure graph. Summarize them into reusable procedures and evidence pointers.

## SKILL.md Integration

Patch the target `SKILL.md` with a short section near the top-level workflow. Keep the exact wording domain-specific, but include this behavior:

```markdown
## Procedural Memory

For tasks that resemble prior episodes, read `references/procedure-memory.md`, inspect `references/procedure-graph.json`, and run `scripts/retrieve_memory.py` with the current task summary before drafting the task plan. Retrieval requires local embeddings and combines 75% normalized RRF score with 25% normalized dense similarity.

Use the retrieval pack to preplay a likely path: review similar failures, select relevant procedure nodes, note reliable transitions, and identify failure patterns to avoid. Treat the preplay as soft guidance; user instructions and fresh task evidence override stale memory.

Default to automatic capture. Before the final response, record a compact episode with `scripts/record_episode.py` when the run contains reusable procedural signal. Include planned trace, executed trace, outcome/reward, productive prefix, failure suffix, procedure candidates, and local validation signal when available.

After recording, run `scripts/refine_graph.py` to update procedure nodes, observed transitions, reward-weighted transition reliability, and failure patterns from the episode. Use local `sentence-transformers` embeddings for task-specific reliability. Do not call paid APIs from refinement scripts.

Do not skip capture unless the user explicitly confirms skipping for this run. If capture seems low-signal, sensitive, or evaluation-contaminating, ask the user to confirm skip; otherwise record a minimal sanitized episode.

End with a procedural-memory receipt: `recorded <episode_id>` or `skipped by explicit user confirmation because <reason>`.
```

If the target skill already has a workflow, insert retrieval before execution and capture after validation but before the final response. If the target skill is tiny, keep the section shorter but preserve retrieval, before-final capture, explicit skip confirmation, and receipt.

## Training Plan

When finishing the scaffold, give the user concrete training instructions:

1. Install or confirm the local embedding backend for `sentence-transformers/all-MiniLM-L6-v2`.
2. Seed memory with 3-5 representative tasks, including at least one failure or correction if available.
3. Run the target skill on one real task at a time.
4. Let the target skill use required dense+RRF retrieval before preplay and auto-record compact memory by default before final response.
5. Let `scripts/refine_graph.py` update procedure nodes, observed edges, reward-weighted reliability records, and failure patterns after each recorded episode.
6. For tasks with local validators, tests, simulators, or benchmark adapters, record observations/actions/rewards as environment signal without paid API calls.
7. For sensitive or held-out episodes, explicitly say whether to skip recording; otherwise the skill should record a sanitized episode.
8. After several updates, run fresh subagent evaluations on held-out prompts.

Give the user copyable prompts such as:

```text
Use $target-skill on this task. Run required embedding+RRF procedural-memory retrieval before preplay and auto-record a compact episode unless I explicitly confirm skipping.
```

```text
For this run, do not record procedural memory. Treat this as explicit confirmation to skip because it is held-out evaluation.
```

```text
Forward-test $target-skill with a fresh Codex subagent on this held-out task. Do not reveal expected answers or prior diagnosis.
```

## Subagent Evaluation

When Codex subagent tools are available, use them for forward-testing after installing or updating the scaffold. If the tools are not already visible, search for multi-agent or subagent tools first.

For before/after comparisons:

- Keep a baseline copy of the target skill before memory changes when practical.
- Run the same held-out task against baseline and scaffolded variants.
- Disable auto-capture only when the user explicitly confirms the held-out evaluation should not be recorded.
- Do not tell subagents which variant is expected to win.
- Pass raw task artifacts, not your diagnosis or intended fix.
- Score hard gates first, then quality, then process compliance.
- Claim improvement only when the scaffolded version wins or ties with a clear reliability, cost, maintainability, or process advantage.

If subagent tools are unavailable, provide the exact prompts the user can run later and say validation is pending.

## Update Policy

Keep procedural memory useful and clean:

- Add a node only for a reusable stage, not a one-off action.
- Add or strengthen an edge only when there is observed evidence from the executed trace, productive prefix, validation result, reward, user correction, or local environment adapter.
- Maintain task-specific transition reliability from local task embeddings and observed reward/outcome weights.
- Record failures as avoidable patterns with context, not blame or vague warnings.
- Auto-record compact episodes by default.
- Ask for explicit user confirmation before skipping; without confirmation, record a minimal sanitized episode.
- Prefer small updates after each episode over large retrospective rewrites.
- Avoid storing private, sensitive, or irrelevant user data in memory.
- Do not add benchmark holdout answers, evaluator rubrics, or hidden expected outputs to memory until the evaluation is no longer meant to be clean.

## Validation

After editing this scaffold or installing it into a target skill, run the mechanical smoke harness when possible:

```bash
python scripts/smoke_test_procedural_memory.py
```

The harness must create a disposable target skill and verify:

- `init_procedural_memory.py` compiles and installs the scaffold with `--patch-skill --force`.
- `references/procedure-memory.md`, `references/procedure-graph.json`, `scripts/retrieve_memory.py`, `scripts/record_episode.py`, and `scripts/refine_graph.py` exist.
- The generated `SKILL.md` contains the Procedural Memory section and refinement instructions.
- The generated graph parses as JSON and has capture, retrieval, refinement, environment-interface, node, edge, episode, and failure-pattern fields.
- Retrieval policy is `hybrid_rrf_dense_reliability`, capture mode is `auto`, skip confirmation is required, and refinement policy is `local_trace_reward_reliability` with no API calls required.
- Generated scripts compile and respond to `--help`.
- Generated scripts do not contain paid/API-call markers such as OpenAI API keys.
- `record_episode.py` can record reward, planned trace, executed trace, lesson, and evidence fields.
- `sentence-transformers` and the configured embedding model must be available; missing embeddings are a failed smoke test, not a skip. `refine_graph.py` must update nodes, edges, and reliability vectors, and `retrieve_memory.py --json` must return `hybrid_rrf_dense_reliability`.

For target-specific validation, also confirm `agents/openai.yaml`, if present, still matches the target skill's purpose, and run any domain-specific tests or validators. Report installed paths, memory files created, retrieval method, embedding model, capture mode, skip-confirmation policy, refinement status, subagent evaluation status, and smoke-test result.

If the user asked only for a scaffold design and not file edits, provide the proposed file tree, patches, and training plan without modifying files.