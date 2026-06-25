# ProPlay Source Map

This reference preserves the source trail for Agentic Skill Scaffolding. Read it before installing or substantially customizing a ProPlay-inspired scaffold.

## Primary Sources

- Paper PDF: https://arxiv.org/pdf/2606.12780
- Paper HTML: https://arxiv.org/html/2606.12780v1
- Repository: https://github.com/antman9914/proplay

## What To Borrow

ProPlay is useful here as an architectural pattern, not as a dependency. For Codex skills, borrow these ideas:

- Preplay before execution: use learned procedural memory to sketch a likely high-level path before starting the task.
- Procedure graph: represent reusable task stages as nodes and useful transitions as edges.
- Reliability records: treat transitions as context-sensitive evidence, not hard rules.
- Episodic refinement: update memory after attempts using success, failure, correction, and validation signal.
- Failure retrieval: consult similar failure patterns before acting so the next run can avoid known traps.
- Soft guidance: let the plan guide the agent while allowing user instructions and fresh observations to override it.

## What Not To Port Directly

Do not copy the repo's benchmark runner into a Codex skill by default. The original implementation is built for programmatic LLM calls and benchmark environments. A Codex-native skill should avoid requiring API keys, long-running autonomous loops, or direct benchmark dependencies unless the user explicitly asks for that setup.

Do not claim that a scaffolded skill has improved merely because memory files were added. Improvement requires held-out evaluation, ideally with fresh Codex subagents.

## Repository Components To Map Conceptually

The ProPlay repository separates the benchmark-agnostic framework from benchmark-specific environments. Map those pieces into Codex skill scaffolding like this:

- Graph logic -> `references/procedure-graph.json` and optional target-local helper scripts.
- Environment interface -> the target skill's existing workflow and available tools.
- LLM client -> the current Codex run or a fresh Codex subagent, not an API call from a script.
- Benchmark folders -> held-out user tasks or representative local artifacts.
- Episode traces -> compact memory updates, not full transcripts.

## Codex-Native Adaptation

A target skill should gain three local files or sections:

1. A short `SKILL.md` Procedural Memory section that says when to read memory, how to preplay, and when to update.
2. `references/procedure-memory.md`, a human-readable guide for the target skill's preplay-execute-refine loop.
3. `references/procedure-graph.json`, a compact machine-readable memory store.

Use `scripts/init_procedural_memory.py` from this skill to create the default files. Then adapt the generated memory reference to the domain.

## Evaluation Pattern

Use fresh Codex subagents as the Codex-native replacement for the repo's programmatic agent runs:

```text
Use $target-skill at <absolute-target-skill-path> to complete this user request:
<held-out task>
```

For clean comparisons, keep a baseline copy of the target skill before adding procedural memory, run the same held-out tasks against baseline and scaffolded variants, and score outputs before drawing conclusions.