# ProPlay Scaffold Template

Use this template when customizing generated procedural memory files for a target skill.

## Target SKILL.md Section

```markdown
## Procedural Memory

For tasks that resemble prior episodes, read `references/procedure-memory.md`, inspect `references/procedure-graph.json`, and run `scripts/retrieve_memory.py` with the current task summary before drafting the task plan. Retrieval requires local embeddings and combines 75% normalized RRF score with 25% normalized dense similarity.

Use the retrieval pack to preplay a likely path: review similar failures, select relevant procedure nodes, note reliable transitions, and identify failure patterns to avoid. Prefer transitions with supporting task-specific reliability when present. Treat the preplay as soft guidance; user instructions and fresh task evidence override stale memory.

Default to automatic capture. Before the final response, record a compact episode with `scripts/record_episode.py` when the run contains reusable procedural signal. Include planned trace, executed trace, outcome/reward, productive prefix, failure suffix, procedure candidates, failure patterns, and local validation or environment signal when available.

After capture, run `scripts/refine_graph.py` to update procedure nodes, observed edges, reward-weighted transition reliability, and failure patterns with local embeddings. Do not call paid APIs from refinement scripts.

Do not skip capture unless the user explicitly confirms skipping for this run. If capture seems low-signal, sensitive, or evaluation-contaminating, ask the user to confirm skip; otherwise record a minimal sanitized episode.

End with a procedural-memory receipt: `recorded <episode_id>` or `skipped by explicit user confirmation because <reason>`.
```

## Procedure Graph Schema

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

## Retrieval Rule

Before preplay, run:

```bash
python scripts/retrieve_memory.py references/procedure-graph.json --query "Current task summary" --top-k 8 --inject-k 3
```

The retriever requires `sentence-transformers/all-MiniLM-L6-v2`, computes RRF over lexical/procedure/failure-pattern rankers, computes dense cosine similarity, computes task-specific transition reliability from locally stored edge reliability vectors when available, normalizes scores, and combines them without paid API calls.

## Auto-Capture Rule

Before the final response, run:

```bash
python scripts/record_episode.py references/procedure-graph.json --task-family example-family --request-summary "Compact task summary" --outcome completed --reward 1.0 --procedure proc_example_stage --planned-trace proc_research,proc_draft --executed-trace proc_research,proc_draft,proc_validate --lesson "Reusable lesson from this run" --evidence-ref current-thread
```

Skipping requires explicit user confirmation for that run:

```text
Procedural memory: skipped by explicit user confirmation because this was a held-out evaluation.
```

Without confirmation, record a minimal sanitized episode rather than skipping.


## Graph Refinement Rule

After recording an episode, update the graph locally:

```bash
python scripts/refine_graph.py references/procedure-graph.json --episode-id episode_id_from_record_episode
```

`refine_graph.py` should add missing reusable procedure nodes from `procedure_candidates` and traces, add or update observed edges from the executed trace or productive prefix, maintain reward-weighted transition reliability vectors using local sentence-transformer embeddings, and add compact failure patterns from failed suffixes. It must not call paid LLM APIs.

For tasks with local validators, tests, simulators, or benchmark wrappers, record their observations/actions/rewards as optional environment signal in the episode before refinement.

## User Training Prompts

```text
Use $target-skill on this task. Run required embedding+RRF procedural-memory retrieval before preplay and auto-record a compact episode unless I explicitly confirm skipping.
```

```text
For this run, do not record procedural memory. Treat this as explicit confirmation to skip because it is held-out evaluation.
```

```text
Forward-test $target-skill with a fresh Codex subagent on this held-out task. Pass only the task and target skill path; do not reveal expected answers or prior diagnosis.
```

## Mechanical Smoke Test

From the `agentic-skill-scaffolding` skill directory, run:

```bash
python scripts/smoke_test_procedural_memory.py
```

The harness creates a disposable target skill, installs the scaffold, checks generated files/schema/script help, records a trace-aware episode, verifies no paid/API-call markers are present in generated scripts, and requires embedding-backed refinement/retrieval to run. Missing `sentence-transformers` or the configured model is a failed smoke test, not a skip.

## Customization Checklist

- Confirm the local embedding dependency is available before relying on retrieval or graph refinement.
- Replace generic task-family names with the target skill's real task families.
- Seed no more than 3-5 initial nodes unless the user provides strong evidence.
- Mark reliability as `unproven` until at least one observed executed trace, reward, validation result, or user correction supports it.
- Keep hidden benchmark answers out of memory until the benchmark is spent.
- Prefer evidence references over copied transcripts.
- Preserve default `retrieval_policy.method = hybrid_rrf_dense_reliability` unless a measured eval proves a better method.
- Preserve default `capture_policy.mode = auto` and `skip_requires_confirmation = true` unless the user explicitly changes the policy.