# ProPlay Scaffold Template

Use this template when customizing generated procedural memory files for a target skill.

## Target SKILL.md Section

```markdown
## Procedural Memory

For tasks that resemble prior episodes, read `references/procedure-memory.md` and inspect `references/procedure-graph.json` before drafting the task plan.

Use the procedure graph to preplay a likely path: select relevant procedure nodes, note reliable transitions, and identify failure patterns to avoid. Treat the preplay as soft guidance; user instructions and fresh task evidence override stale memory.

Default to automatic capture. Before the final response, record a compact episode with `scripts/record_episode.py` when the run contains reusable procedural signal. Skip only when the episode is low-signal, sensitive beyond safe summarization, or part of a held-out evaluation that should remain uncontaminated.

End with a procedural-memory receipt: `recorded <episode_id>` or `skipped because <reason>`.
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
    "sensitive_data": "summarize_or_skip"
  },
  "nodes": [
    {
      "id": "proc_example_stage",
      "label": "Example stage",
      "description": "Reusable task stage.",
      "task_families": ["example-family"],
      "evidence": []
    }
  ],
  "edges": [
    {
      "id": "edge_example_stage_to_next",
      "from": "proc_example_stage",
      "to": "proc_next_stage",
      "condition": "When this transition is useful.",
      "reliability": "unproven|emerging|reliable|contested",
      "evidence": []
    }
  ],
  "episodes": [
    {
      "id": "episode_YYYYMMDD_short_slug",
      "task_family": "example-family",
      "request_summary": "Compact description of the task.",
      "outcome": "success|partial|failure|completed|skipped",
      "procedures_used": ["proc_example_stage"],
      "lessons": ["Reusable lesson only."],
      "failure_patterns": [],
      "sensitivity": "none|summarized|skipped_sensitive",
      "evidence_ref": "Where to find the source artifact or user correction, if safe to store."
    }
  ],
  "failure_patterns": [
    {
      "id": "fail_example",
      "pattern": "The avoidable failure.",
      "context": "When it appears.",
      "avoidance": "What to do instead.",
      "evidence": []
    }
  ]
}
```

## Auto-Capture Rule

Before the final response, the target skill should do one of these:

```bash
python scripts/record_episode.py references/procedure-graph.json --episode-json '{"id":"episode_YYYYMMDD_short_slug","task_family":"example-family","request_summary":"...","outcome":"completed","procedures_used":[],"lessons":[],"failure_patterns":[],"sensitivity":"none","evidence_ref":"current-thread"}'
```

or explicitly skip with a final receipt:

```text
Procedural memory: skipped because this was a held-out evaluation.
```

## User Training Prompts

```text
Use $target-skill on this task and auto-record a compact procedural-memory episode unless it is low-signal or sensitive.
```

```text
Record this as a successful $target-skill training episode. Update only reusable procedure nodes, transitions, and failure-avoidance notes.
```

```text
Record this correction as $target-skill procedural memory. Preserve the correction's lesson but do not store unnecessary personal or confidential details.
```

```text
For this run, do not record procedural memory. Treat it as held-out evaluation.
```

```text
Forward-test $target-skill with a fresh Codex subagent on this held-out task. Pass only the task and target skill path; do not reveal expected answers or prior diagnosis.
```

## Customization Checklist

- Replace generic task-family names with the target skill's real task families.
- Seed no more than 3-5 initial nodes unless the user provides strong evidence.
- Mark reliability as `unproven` until at least one observed episode supports it.
- Keep hidden benchmark answers out of memory until the benchmark is spent.
- Prefer evidence references over copied transcripts.
- Preserve the default `auto` capture policy unless the target domain has privacy or evaluation reasons to use `confirm` or `manual`.